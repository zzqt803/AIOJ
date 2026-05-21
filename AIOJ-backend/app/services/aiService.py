import json
from anthropic import Anthropic
from app.core.config import settings
from app.models.submissions import Submission, AIAnalysisStatusEnum
from app.models.problems import Problem
from sqlalchemy.orm import Session

# AI 分析提示词模板
ANALYSIS_PROMPT = """你是一个专业的编程助手和代码审查专家。请分析以下代码提交，并给出详细的反馈。语言要温柔体贴。

## 题目信息
- 题目ID: {problem_id}
- 题目标题: {problem_title}
- 题目描述: {problem_description}
- 时间限制: {time_limit}ms
- 内存限制: {memory_limit}MB
- 样例输入：{sample_input}
- 样例输入：{sample_output}

## 提交信息
- 语言: {language}
- 评测结果: {result}
- 执行时间: {time_used}ms
- 内存使用: {memory_used}KB

## 用户代码
```{language}
{code}
```

## 测试点详情
{test_case_details}

请按照以下 JSON 格式返回分析结果：
{{
    "summary": "对代码的整体评价（2-3句话）",
    "time_complexity": "时间复杂度，如 O(n)",
    "space_complexity": "空间复杂度，如 O(1)",
    "issues": [
        {{
            "line": 问题所在行号（如果没有具体行号则为 null）,
            "description": "问题描述"
        }}
    ],
    "suggestions": ["改进建议1", "改进建议2"],
    "score": 代码质量评分（0-100）
}}

注意：
1. 如果代码通过了所有测试，重点给出优化建议和代码质量改进
2. 如果代码未通过，分析可能的原因并给出修改方向
3. 如果有编译错误或运行时错误，帮助分析错误原因
4. 建议要具体可操作，不要泛泛而谈
5. 评分标准：功能正确性(40%) + 代码质量(30%) + 效率(20%) + 可读性(10%)
6. 语言要温柔，用户可能只是什么都不会的小白，要温柔的引导
"""


def analyze_submission_sync(submission_id: int, db: Session):
    """同步分析提交结果并调用 AI 生成建议"""

    # 获取提交信息
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        return

    # 获取题目信息
    problem = db.query(Problem).filter(Problem.id == submission.problem_id).first()
    if not problem:
        return

    # 更新状态为分析中
    submission.ai_analysis_status = AIAnalysisStatusEnum.analyzing
    db.commit()

    try:
        # 格式化测试点详情
        test_case_details = "无测试点详情"
        if submission.test_case_details:
            details = []
            for tc in submission.test_case_details:
                status_map = {
                    "accepted": "通过",
                    "wrong_answer": "答案错误",
                    "runtime_error": "运行时错误",
                    "time_limit": "超时",
                    "memory_limit": "内存超限",
                    "compile_error": "编译错误",
                    "system_error": "系统错误",
                }
                status = status_map.get(tc.get("status", ""), tc.get("status", ""))
                detail = f"- 测试点 {tc.get('test_case_id', '?')}: {status}"
                if tc.get("time_used_ms"):
                    detail += f" (耗时: {tc['time_used_ms']}ms"
                if tc.get("memory_used_kb"):
                    detail += f", 内存: {tc['memory_used_kb']}KB)"
                elif tc.get("time_used_ms"):
                    detail += ")"
                if tc.get("error_message"):
                    detail += f"\n  错误信息: {tc['error_message']}"
                details.append(detail)
            test_case_details = "\n".join(details)

        # 构建提示词
        prompt = ANALYSIS_PROMPT.format(
            problem_id=submission.problem_id,
            problem_title=problem.title,
            problem_description=problem.description[:500],
            time_limit=problem.time_limit,
            memory_limit=problem.memory_limit,
            sample_input=problem.sample_input,
            sample_output=problem.sample_output,
            language=submission.language,
            result=submission.result.value if submission.result else "未知",
            time_used=submission.time_used or 0,
            memory_used=submission.memory_used or 0,
            code=submission.code[:3000],
            test_case_details=test_case_details,
        )

        # 调用 AI API
        ai_result = call_ai_api(prompt)

        # 更新结果
        submission.ai_analysis_status = AIAnalysisStatusEnum.completed
        submission.ai_analysis_result = ai_result
        db.commit()

    except Exception as e:
        print(f"AI analysis failed for submission {submission_id}: {e}")
        submission.ai_analysis_status = AIAnalysisStatusEnum.pending
        db.commit()


def call_ai_api(prompt: str) -> dict:
    """调用 AI API 获取分析结果"""

    api_key = settings.AI_API_KEY
    model = settings.AI_MODEL
    base_url = settings.AI_BASE_URL

    if not api_key:
        raise ValueError("AI API 配置未设置")

    client = Anthropic(api_key=api_key, base_url=base_url)

    response = client.messages.create(
        model=model,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
        system="你是一个专业的编程助手，擅长代码分析和优化建议。请始终返回有效的 JSON 格式。",
    )

    content = response.content[0].text

    # 解析 JSON 响应
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # 如果包含 markdown 代码块，提取 JSON 部分
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
            return json.loads(json_str)
        else:
            return {
                "summary": content[:200],
                "time_complexity": "未知",
                "space_complexity": "未知",
                "issues": [],
                "suggestions": ["无法解析 AI 响应，请重试"],
                "score": 0,
            }
