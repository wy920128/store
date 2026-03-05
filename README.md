<!--
 * @Author: 王野 18545455617@163.com
 * @Date: 2026-03-04 16:35:26
 * @LastEditors: 王野 18545455617@163.com
 * @LastEditTime: 2026-03-05 16:36:28
 * @FilePath: /store/README.md
 * @Description: README.md
-->

3. 数据库语句
   -- 创建数据库
   CREATE DATABASE IF NOT EXISTS store
   DEFAULT CHARACTER SET utf8mb4
   COLLATE utf8mb4_unicode_ci;

   USE store;

   -- 1. 创建分类表(classify)
   CREATE TABLE IF NOT EXISTS classify (
   id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY COMMENT '分类主键 ID',
   name VARCHAR(64) NOT NULL COMMENT '分类名称（唯一）',
   description VARCHAR(255) DEFAULT NULL COMMENT '分类描述',
   created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
   deleted_time TIMESTAMP NULL DEFAULT NULL COMMENT '软删除标记',
   UNIQUE INDEX uk_name_deleted (name, deleted_time),
   INDEX idx_name (name),
   INDEX idx_deleted_time (deleted_time)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='软件分类表';

   -- 2. 创建软件表(software)
   CREATE TABLE IF NOT EXISTS software (
   id CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY COMMENT '软件主键 ID',
   name VARCHAR(128) NOT NULL COMMENT '软件名称',
   version VARCHAR(32) DEFAULT NULL COMMENT '软件版本',
   size VARCHAR(64) DEFAULT NULL COMMENT '软件大小',
   download_url VARCHAR(255) DEFAULT NULL COMMENT '下载链接',
   provider_department VARCHAR(128) DEFAULT NULL COMMENT '提供单位',
   provider VARCHAR(64) DEFAULT NULL COMMENT '提供者',
   created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
   updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
   deleted_time TIMESTAMP NULL DEFAULT NULL COMMENT '软删除标记',
   INDEX idx_name_deleted (name, deleted_time),
   INDEX idx_deleted_time (deleted_time)
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='软件信息表';

   -- 3. 创建分类关联软件表(classify2software)
   CREATE TABLE IF NOT EXISTS classify2software (
   classify_id INT UNSIGNED NOT NULL COMMENT '分类ID',
   software_id CHAR(36) NOT NULL COMMENT '软件ID',
   created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '关联创建时间',
   deleted_time TIMESTAMP NULL DEFAULT NULL COMMENT '软删除标记（NULL=未删除，非NULL=删除时间）',
   UNIQUE INDEX uk_classify_software_deleted (classify_id, software_id, deleted_time),
   INDEX idx_classify_id (classify_id),
   INDEX idx_software_id (software_id),
   INDEX idx_deleted_time (deleted_time),
   FOREIGN KEY (classify_id) REFERENCES classify(id) ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY (software_id) REFERENCES software(id) ON DELETE CASCADE ON UPDATE CASCADE
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='分类关联软件表';
