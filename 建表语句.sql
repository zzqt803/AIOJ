-- ============================================
-- AIOJ 智能在线判题平台 - 建表语句
-- 数据库: MySQL 8.0+
-- 字符集: utf8mb4
-- 支持重复执行（IF NOT EXISTS）
-- ============================================

CREATE DATABASE IF NOT EXISTS aioj DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aioj;

-- ============================================
-- 1. 用户表
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id            INT          NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    username      VARCHAR(50)  NOT NULL COMMENT '用户名',
    email         VARCHAR(100) NOT NULL COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    role          ENUM('admin', 'user', 'guest') NOT NULL DEFAULT 'user' COMMENT '用户角色',
    is_active     TINYINT(1)   NOT NULL DEFAULT 1 COMMENT '是否启用',
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (id),
    UNIQUE KEY uk_username (username),
    UNIQUE KEY uk_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- ============================================
-- 2. 题目表
-- ============================================
CREATE TABLE IF NOT EXISTS problems (
    id            INT          NOT NULL AUTO_INCREMENT COMMENT '题目ID',
    title         VARCHAR(100) NOT NULL COMMENT '题目标题',
    difficulty    ENUM('easy', 'medium', 'hard') NOT NULL DEFAULT 'easy' COMMENT '题目难度',
    tags          JSON         NOT NULL COMMENT '题目标签列表',
    description   TEXT         NOT NULL COMMENT '题目描述',
    input_format  TEXT         NOT NULL COMMENT '输入格式说明',
    output_format TEXT         NOT NULL COMMENT '输出格式说明',
    sample_input  TEXT         NOT NULL COMMENT '样例输入',
    sample_output TEXT         NOT NULL COMMENT '样例输出',
    hint          TEXT         NULL COMMENT '提示/解题思路',
    time_limit    INT          NOT NULL DEFAULT 1000 COMMENT '时间限制（毫秒）',
    memory_limit  INT          NOT NULL DEFAULT 256 COMMENT '内存限制（MB）',
    is_public     TINYINT(1)   NOT NULL DEFAULT 1 COMMENT '是否公开',
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    INDEX idx_difficulty (difficulty),
    INDEX idx_is_public (is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题目表';

-- ============================================
-- 3. 提交表
-- ============================================
CREATE TABLE IF NOT EXISTS submissions (
    id                 INT                                     NOT NULL AUTO_INCREMENT COMMENT '提交ID',
    user_id            INT                                     NOT NULL COMMENT '用户ID',
    problem_id         INT                                     NOT NULL COMMENT '题目ID',
    language           VARCHAR(20)                             NOT NULL COMMENT '编程语言',
    code               TEXT                                    NOT NULL COMMENT '代码内容',
    status             ENUM('pending', 'completed')           NOT NULL DEFAULT 'pending' COMMENT '判题状态',
    result             ENUM('passed', 'attempted')             NULL COMMENT '总体评测结果',
    time_used          INT                                     NULL COMMENT '总耗时（毫秒）',
    memory_used        INT                                     NULL COMMENT '最大内存使用（KB）',
    test_case_details  JSON                                    NULL COMMENT '测试点详情',
    compile_error      TEXT                                    NULL COMMENT '编译错误信息',
    ai_analysis_status ENUM('pending', 'analyzing', 'completed') NOT NULL DEFAULT 'pending' COMMENT 'AI分析状态',
    ai_analysis_result JSON                                    NULL COMMENT 'AI分析结果',
    created_at         DATETIME                                NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_problem_id (problem_id),
    INDEX idx_status (status),
    INDEX idx_user_problem (user_id, problem_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='提交表';

-- ============================================
-- 4. 题单表
-- ============================================
CREATE TABLE IF NOT EXISTS problem_sets (
    id          INT          NOT NULL AUTO_INCREMENT COMMENT '题单ID',
    title       VARCHAR(100) NOT NULL COMMENT '题单标题',
    description TEXT         NULL COMMENT '题单描述',
    creator_id  INT          NOT NULL COMMENT '创建者ID',
    is_public   TINYINT(1)   NOT NULL DEFAULT 1 COMMENT '是否公开',
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_creator_id (creator_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题单表';

-- ============================================
-- 5. 题单条目表（题单-题目关联）
-- ============================================
CREATE TABLE IF NOT EXISTS problem_set_items (
    id             INT NOT NULL AUTO_INCREMENT COMMENT '关联ID',
    problem_set_id INT NOT NULL COMMENT '题单ID',
    problem_id     INT NOT NULL COMMENT '题目ID',
    sort_order     INT NOT NULL DEFAULT 0 COMMENT '排序序号',
    PRIMARY KEY (id),
    FOREIGN KEY (problem_set_id) REFERENCES problem_sets(id) ON DELETE CASCADE,
    FOREIGN KEY (problem_id)     REFERENCES problems(id)     ON DELETE CASCADE,
    UNIQUE KEY uk_set_problem (problem_set_id, problem_id),
    INDEX idx_problem_id (problem_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题单条目表';

-- ============================================
-- 6. 讨论表
-- ============================================
CREATE TABLE IF NOT EXISTS discussions (
    id         INT      NOT NULL AUTO_INCREMENT COMMENT '评论ID',
    problem_id INT      NOT NULL COMMENT '题目ID',
    user_id    INT      NOT NULL COMMENT '用户ID',
    content    TEXT     NOT NULL COMMENT '评论内容',
    parent_id  INT      NULL COMMENT '父评论ID，NULL为一级评论',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    FOREIGN KEY (problem_id) REFERENCES problems(id)    ON DELETE CASCADE,
    FOREIGN KEY (user_id)    REFERENCES users(id)       ON DELETE CASCADE,
    FOREIGN KEY (parent_id)  REFERENCES discussions(id)  ON DELETE CASCADE,
    INDEX idx_problem_id (problem_id),
    INDEX idx_user_id (user_id),
    INDEX idx_parent_id (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='讨论表';

-- ============================================
-- 7. 用户统计表
-- ============================================
CREATE TABLE IF NOT EXISTS user_stats (
    id                  INT      NOT NULL AUTO_INCREMENT COMMENT '统计ID',
    user_id             INT      NOT NULL COMMENT '用户ID',
    total_submissions   INT      NOT NULL DEFAULT 0 COMMENT '总提交次数',
    accepted_submissions INT     NOT NULL DEFAULT 0 COMMENT '通过次数',
    solved_problems     INT      NOT NULL DEFAULT 0 COMMENT '已解决题目数',
    easy_solved         INT      NOT NULL DEFAULT 0 COMMENT '简单题通过数',
    medium_solved       INT      NOT NULL DEFAULT 0 COMMENT '中等题通过数',
    hard_solved         INT      NOT NULL DEFAULT 0 COMMENT '困难题通过数',
    max_streak          INT      NOT NULL DEFAULT 0 COMMENT '最大连续刷题天数',
    current_streak      INT      NOT NULL DEFAULT 0 COMMENT '当前连续刷题天数',
    last_active_date    DATE     NULL COMMENT '最后活跃日期',
    updated_at          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户统计表';

-- ============================================
-- 8. 收藏表
-- ============================================
CREATE TABLE IF NOT EXISTS bookmarks (
    id         INT      NOT NULL AUTO_INCREMENT COMMENT '收藏ID',
    user_id    INT      NOT NULL COMMENT '用户ID',
    problem_id INT      NOT NULL COMMENT '题目ID',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间',
    PRIMARY KEY (id),
    FOREIGN KEY (user_id)    REFERENCES users(id)    ON DELETE CASCADE,
    FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE,
    UNIQUE KEY uk_user_problem (user_id, problem_id),
    INDEX idx_user_id (user_id),
    INDEX idx_problem_id (problem_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='收藏表';


-- ============================================
-- 视图（先删后建，避免重复报错）
-- ============================================

DROP VIEW IF EXISTS v_problem_stats;
CREATE VIEW v_problem_stats AS
SELECT
    p.id            AS problem_id,
    p.title,
    p.difficulty,
    COUNT(s.id)                                         AS total_submissions,
    SUM(CASE WHEN s.result = 'passed' THEN 1 ELSE 0 END) AS accepted_count,
    ROUND(
        SUM(CASE WHEN s.result = 'passed' THEN 1 ELSE 0 END) / NULLIF(COUNT(s.id), 0) * 100,
        2
    )                                                   AS accept_rate
FROM problems p
LEFT JOIN submissions s ON s.problem_id = p.id AND s.status = 'completed'
GROUP BY p.id, p.title, p.difficulty;

DROP VIEW IF EXISTS v_user_leaderboard;
CREATE VIEW v_user_leaderboard AS
SELECT
    u.id                AS user_id,
    u.username,
    us.solved_problems,
    us.easy_solved,
    us.medium_solved,
    us.hard_solved,
    us.total_submissions,
    us.max_streak,
    us.current_streak
FROM users u
JOIN user_stats us ON us.user_id = u.id
WHERE u.is_active = 1 AND u.role = 'user'
ORDER BY us.solved_problems DESC, us.accepted_submissions ASC;

DROP VIEW IF EXISTS v_problem_set_summary;
CREATE VIEW v_problem_set_summary AS
SELECT
    ps.id           AS problem_set_id,
    ps.title,
    ps.creator_id,
    u.username      AS creator_name,
    ps.is_public,
    COUNT(psi.id)   AS problem_count,
    ps.created_at
FROM problem_sets ps
JOIN users u ON u.id = ps.creator_id
LEFT JOIN problem_set_items psi ON psi.problem_set_id = ps.id
GROUP BY ps.id, ps.title, ps.creator_id, u.username, ps.is_public, ps.created_at;


-- ============================================
-- 触发器（先删后建）
-- ============================================

DROP TRIGGER IF EXISTS trg_after_user_insert;
DELIMITER //
CREATE TRIGGER trg_after_user_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO user_stats (user_id) VALUES (NEW.id);
END //
DELIMITER ;

DROP TRIGGER IF EXISTS trg_after_submission_update;
DELIMITER //
CREATE TRIGGER trg_after_submission_update
AFTER UPDATE ON submissions
FOR EACH ROW
BEGIN
    IF NEW.status = 'completed' AND NEW.result = 'passed' AND OLD.status = 'pending' THEN
        SET @first_pass = (
            SELECT COUNT(*) FROM submissions
            WHERE user_id = NEW.user_id
              AND problem_id = NEW.problem_id
              AND result = 'passed'
              AND id < NEW.id
        );

        UPDATE user_stats SET
            total_submissions = total_submissions + 1,
            accepted_submissions = accepted_submissions + 1,
            solved_problems     = solved_problems + CASE WHEN @first_pass = 0 THEN 1 ELSE 0 END,
            easy_solved         = easy_solved + CASE WHEN @first_pass = 0 AND (SELECT difficulty FROM problems WHERE id = NEW.problem_id) = 'easy' THEN 1 ELSE 0 END,
            medium_solved       = medium_solved + CASE WHEN @first_pass = 0 AND (SELECT difficulty FROM problems WHERE id = NEW.problem_id) = 'medium' THEN 1 ELSE 0 END,
            hard_solved         = hard_solved + CASE WHEN @first_pass = 0 AND (SELECT difficulty FROM problems WHERE id = NEW.problem_id) = 'hard' THEN 1 ELSE 0 END,
            last_active_date    = CURDATE()
        WHERE user_id = NEW.user_id;
    ELSEIF NEW.status = 'completed' AND OLD.status = 'pending' THEN
        UPDATE user_stats SET
            total_submissions = total_submissions + 1,
            last_active_date  = CURDATE()
        WHERE user_id = NEW.user_id;
    END IF;
END //
DELIMITER ;


-- ============================================
-- 存储过程（先删后建）
-- ============================================

DROP PROCEDURE IF EXISTS sp_update_streak;
DELIMITER //
CREATE PROCEDURE sp_update_streak()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_user_id INT;
    DECLARE v_last_active DATE;
    DECLARE v_current_streak INT;
    DECLARE cur CURSOR FOR SELECT user_id, last_active_date, current_streak FROM user_stats;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_user_id, v_last_active, v_current_streak;
        IF done THEN LEAVE read_loop; END IF;

        IF v_last_active = CURDATE() THEN
            ITERATE read_loop;
        ELSEIF v_last_active = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN
            ITERATE read_loop;
        ELSE
            UPDATE user_stats SET current_streak = 0 WHERE user_id = v_user_id;
        END IF;
    END LOOP;
    CLOSE cur;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_get_problem_stats;
DELIMITER //
CREATE PROCEDURE sp_get_problem_stats(IN p_problem_id INT)
BEGIN
    SELECT
        p.id            AS problem_id,
        p.title,
        p.difficulty,
        COUNT(s.id)                                             AS total_submissions,
        SUM(CASE WHEN s.result = 'passed' THEN 1 ELSE 0 END)  AS accepted_count,
        COUNT(DISTINCT CASE WHEN s.result = 'passed' THEN s.user_id END) AS solved_users,
        ROUND(
            SUM(CASE WHEN s.result = 'passed' THEN 1 ELSE 0 END) / NULLIF(COUNT(s.id), 0) * 100,
            2
        ) AS accept_rate
    FROM problems p
    LEFT JOIN submissions s ON s.problem_id = p.id AND s.status = 'completed'
    WHERE p.id = p_problem_id
    GROUP BY p.id, p.title, p.difficulty;
END //
DELIMITER ;
