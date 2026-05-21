import json
import threading
from app.db.redis import redis_client
from app.db.session import SessionLocal
from app.core.config import settings
from app.models.submissions import Submission, StatusEnum, OverallResultEnum
from app.services.aiService import analyze_submission_sync


def process_result(result_data: dict):
    """处理判题结果，更新数据库并触发 AI 分析"""
    db = SessionLocal()
    try:
        submission_id = int(result_data.get("submission_id", 0))
        if not submission_id:
            return

        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            return

        # 更新状态为已完成
        submission.status = StatusEnum.completed

        # 判断总体结果：全部通过=passed，否则=attempted
        overall_status = result_data.get("overall_status", "")
        if overall_status == "accepted":
            submission.result = OverallResultEnum.passed
        else:
            submission.result = OverallResultEnum.attempted

        # 更新时间和内存（直接存储毫秒和KB）
        submission.time_used = result_data.get("total_time_ms", 0)
        submission.memory_used = result_data.get("max_memory_kb", 0)

        # 保存测试点详情
        details = result_data.get("details", [])
        submission.test_case_details = details

        db.commit()
        print(f"Submission {submission_id} updated: {submission.result.value}")

        # 触发 AI 分析（同步执行）
        analyze_submission_sync(submission_id, db)

    except Exception as e:
        db.rollback()
        print(f"Error processing result: {e}")
    finally:
        db.close()


def result_consumer_worker():
    """结果消费者线程"""
    print(f"Result consumer started, listening on {settings.RESULT_QUEUE}")
    while True:
        try:
            # BRPOP 阻塞等待结果
            result = redis_client.brpop(settings.RESULT_QUEUE, timeout=5)
            if result:
                _, data = result
                result_data = json.loads(data)
                process_result(result_data)
        except Exception as e:
            print(f"Consumer error: {e}")


def start_result_consumer():
    """启动结果消费者线程"""
    thread = threading.Thread(target=result_consumer_worker, daemon=True)
    thread.start()
    print("Result consumer thread started")
