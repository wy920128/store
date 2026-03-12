/*
 Navicat Premium Dump SQL

 Source Server         : MariaDB_阿里云
 Source Server Type    : MariaDB
 Source Server Version : 120102 (12.1.2-MariaDB)
 Source Host           : 182.92.221.228:6603
 Source Schema         : uos

 Target Server Type    : MariaDB
 Target Server Version : 120102 (12.1.2-MariaDB)
 File Encoding         : 65001

 Date: 10/03/2026 14:12:14
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for category
-- ----------------------------
DROP TABLE IF EXISTS `category`;
CREATE TABLE `category`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分类主键 ID',
  `name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NOT NULL COMMENT '分类名称（唯一）',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NULL DEFAULT NULL COMMENT '分类描述',
  `created_time` timestamp NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `updated_time` timestamp NULL DEFAULT current_timestamp() ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_time` timestamp NULL DEFAULT NULL COMMENT '软删除标记',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_name_deleted`(`name` ASC, `deleted_time` ASC) USING BTREE,
  INDEX `idx_name`(`name` ASC) USING BTREE,
  INDEX `idx_deleted_time`(`deleted_time` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci COMMENT = '软件分类表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of category
-- ----------------------------
INSERT INTO `category` VALUES (1, '办公软件', '日常办公所需的各类工具软件，包含文字处理、表格制作、演示文稿等', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `category` VALUES (2, '设计软件', '图形设计、图像处理、视频剪辑等创意设计类软件', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `category` VALUES (3, '开发工具', '编程开发、代码调试、版本管理等开发者工具', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `category` VALUES (4, '系统工具', '系统优化、文件管理、硬件检测等系统级工具', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `category` VALUES (5, '网络工具', '浏览器、下载工具、网络测速等网络相关软件', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `category` VALUES (6, '教育学习', '在线学习、题库练习、语言学习等教育类软件', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `category` VALUES (7, '娱乐休闲', '影音播放、游戏、小说阅读等休闲娱乐软件', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);

-- ----------------------------
-- Table structure for category2software
-- ----------------------------
DROP TABLE IF EXISTS `category2software`;
CREATE TABLE `category2software`  (
  `classify_id` int(10) UNSIGNED NOT NULL COMMENT '分类ID',
  `software_id` char(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NOT NULL COMMENT '软件ID',
  `created_time` timestamp NULL DEFAULT current_timestamp() COMMENT '关联创建时间',
  `deleted_time` timestamp NULL DEFAULT NULL COMMENT '软删除标记（NULL=未删除，非NULL=删除时间）',
  UNIQUE INDEX `uk_classify_software_deleted`(`classify_id` ASC, `software_id` ASC, `deleted_time` ASC) USING BTREE,
  INDEX `idx_classify_id`(`classify_id` ASC) USING BTREE,
  INDEX `idx_software_id`(`software_id` ASC) USING BTREE,
  INDEX `idx_deleted_time`(`deleted_time` ASC) USING BTREE,
  CONSTRAINT `1` FOREIGN KEY (`classify_id`) REFERENCES `category` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `2` FOREIGN KEY (`software_id`) REFERENCES `software` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci COMMENT = '分类关联软件表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of category2software
-- ----------------------------
INSERT INTO `category2software` VALUES (1, '9298c892-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '9299789d-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '9299dda8-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929a44d0-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929aa8ec-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929b0c96-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929b7416-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929bd94e-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929c60c0-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929cc5b1-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929d2b52-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929d93fb-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929df716-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929e5e45-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (1, '929eac9c-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92ae781c-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92aeed1c-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92af53b5-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92afb87d-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92b020ed-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92b08de5-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92b1213c-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92b18697-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92b1e9b7-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92b24db1-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92b2b47e-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92b317f6-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (2, '92b37c19-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:15', NULL);
INSERT INTO `category2software` VALUES (3, '92c2c94e-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c33748-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c39d27-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c4074c-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c46c0f-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c4d0a1-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c53430-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c5a116-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c606b0-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c65563-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c6ab90-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c70fdb-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (3, '92c77851-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d42b99-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d496e1-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d4ffdd-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d56438-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d5d180-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d63728-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d6e973-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d74edd-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d79c53-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d7e965-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d853e7-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d8efad-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (4, '92d9542b-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92e6e64a-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92e7548a-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92e7ba84-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92e828b4-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92e88d31-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92e8f217-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92e9611a-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92e9c596-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92ea2819-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92ea8d2b-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92eaf13e-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92eb3d96-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (5, '92eba5f7-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fb09cb-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fb7b03-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fbcdac-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fc3605-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fc861d-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fcee70-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fd4104-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fda811-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fdf893-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92fe5f20-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92feb0d6-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92ff1f47-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (6, '92ff71fa-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '930f3111-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '930f9dac-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '93103692-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '93109cdf-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '9311039d-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '93116775-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '9311db13-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '93123ed3-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '9312a7fd-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '93130fee-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '93135eb6-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '9313abb3-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);
INSERT INTO `category2software` VALUES (7, '931411e7-1c28-11f1-a27a-00163e1435d4', '2026-03-10 10:27:16', NULL);

-- ----------------------------
-- Table structure for software
-- ----------------------------
DROP TABLE IF EXISTS `software`;
CREATE TABLE `software`  (
  `id` char(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NOT NULL DEFAULT uuid() COMMENT '软件主键 ID',
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NOT NULL COMMENT '软件名称',
  `version` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NULL DEFAULT NULL COMMENT '软件版本',
  `size` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NULL DEFAULT NULL COMMENT '软件大小',
  `download_count` int(11) NULL DEFAULT NULL COMMENT '下载量',
  `download_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NULL DEFAULT NULL COMMENT '下载链接',
  `provider_department` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NULL DEFAULT NULL COMMENT '提供单位',
  `provider` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NULL DEFAULT NULL COMMENT '提供者',
  `created_time` timestamp NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `updated_time` timestamp NULL DEFAULT current_timestamp() ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_time` timestamp NULL DEFAULT NULL COMMENT '软删除标记',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_name_deleted`(`name` ASC, `deleted_time` ASC) USING BTREE,
  INDEX `idx_deleted_time`(`deleted_time` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci COMMENT = '软件信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of software
-- ----------------------------
INSERT INTO `software` VALUES ('9298c892-1c28-11f1-a27a-00163e1435d4', 'UOS办公-1', '2.7.0', '84MB', 13079, 'https://download.uos.com/uos办公1.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('9299789d-1c28-11f1-a27a-00163e1435d4', 'UOS办公-2', '2.5.5', '135MB', 99293, 'https://download.uos.com/uos办公2.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('9299dda8-1c28-11f1-a27a-00163e1435d4', 'UOS办公-3', '3.7.1', '379MB', 49046, 'https://download.uos.com/uos办公3.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929a44d0-1c28-11f1-a27a-00163e1435d4', 'UOS办公-4', '2.0.2', '118MB', 84827, 'https://download.uos.com/uos办公4.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929aa8ec-1c28-11f1-a27a-00163e1435d4', 'UOS办公-5', '5.8.4', '818MB', 71273, 'https://download.uos.com/uos办公5.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929b0c96-1c28-11f1-a27a-00163e1435d4', 'UOS办公-6', '1.3.4', '18MB', 84601, 'https://download.uos.com/uos办公6.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929b7416-1c28-11f1-a27a-00163e1435d4', 'UOS办公-7', '1.2.8', '609MB', 36162, 'https://download.uos.com/uos办公7.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929bd94e-1c28-11f1-a27a-00163e1435d4', 'UOS办公-8', '5.7.8', '18MB', 50455, 'https://download.uos.com/uos办公8.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929c60c0-1c28-11f1-a27a-00163e1435d4', 'UOS办公-9', '3.7.4', '869MB', 3531, 'https://download.uos.com/uos办公9.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929cc5b1-1c28-11f1-a27a-00163e1435d4', 'UOS办公-10', '3.6.6', '455MB', 16922, 'https://download.uos.com/uos办公10.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929d2b52-1c28-11f1-a27a-00163e1435d4', 'UOS办公-11', '3.8.7', '189MB', 71917, 'https://download.uos.com/uos办公11.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929d93fb-1c28-11f1-a27a-00163e1435d4', 'UOS办公-12', '1.9.5', '1007MB', 35116, 'https://download.uos.com/uos办公12.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929df716-1c28-11f1-a27a-00163e1435d4', 'UOS办公-13', '4.5.5', '344MB', 89586, 'https://download.uos.com/uos办公13.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929e5e45-1c28-11f1-a27a-00163e1435d4', 'UOS办公-14', '3.4.0', '11MB', 76467, 'https://download.uos.com/uos办公14.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('929eac9c-1c28-11f1-a27a-00163e1435d4', 'UOS办公-15', '4.5.6', '359MB', 89155, 'https://download.uos.com/uos办公15.exe', 'UOS软件研发部-办公软件组', 'UOS官方-UOS办', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92ae781c-1c28-11f1-a27a-00163e1435d4', 'UOS设计-1', '2.1.6', '1007MB', 92279, 'https://download.uos.com/uos设计1.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92aeed1c-1c28-11f1-a27a-00163e1435d4', 'UOS设计-2', '3.1.8', '956MB', 17074, 'https://download.uos.com/uos设计2.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92af53b5-1c28-11f1-a27a-00163e1435d4', 'UOS设计-3', '5.3.7', '939MB', 29463, 'https://download.uos.com/uos设计3.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92afb87d-1c28-11f1-a27a-00163e1435d4', 'UOS设计-4', '4.3.7', '592MB', 79069, 'https://download.uos.com/uos设计4.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92b020ed-1c28-11f1-a27a-00163e1435d4', 'UOS设计-5', '1.4.7', '317MB', 37325, 'https://download.uos.com/uos设计5.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92b08de5-1c28-11f1-a27a-00163e1435d4', 'UOS设计-6', '5.3.2', '959MB', 10482, 'https://download.uos.com/uos设计6.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92b1213c-1c28-11f1-a27a-00163e1435d4', 'UOS设计-7', '4.8.3', '124MB', 59918, 'https://download.uos.com/uos设计7.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92b18697-1c28-11f1-a27a-00163e1435d4', 'UOS设计-8', '4.2.4', '477MB', 1328, 'https://download.uos.com/uos设计8.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92b1e9b7-1c28-11f1-a27a-00163e1435d4', 'UOS设计-9', '4.0.4', '235MB', 68311, 'https://download.uos.com/uos设计9.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92b24db1-1c28-11f1-a27a-00163e1435d4', 'UOS设计-10', '4.4.0', '60MB', 6378, 'https://download.uos.com/uos设计10.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92b2b47e-1c28-11f1-a27a-00163e1435d4', 'UOS设计-11', '1.4.7', '630MB', 77234, 'https://download.uos.com/uos设计11.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92b317f6-1c28-11f1-a27a-00163e1435d4', 'UOS设计-12', '5.4.4', '971MB', 40525, 'https://download.uos.com/uos设计12.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92b37c19-1c28-11f1-a27a-00163e1435d4', 'UOS设计-13', '1.2.0', '608MB', 75339, 'https://download.uos.com/uos设计13.exe', 'UOS软件研发部-设计软件组', 'UOS官方-UOS设', '2026-03-10 10:27:15', '2026-03-10 10:27:15', NULL);
INSERT INTO `software` VALUES ('92c2c94e-1c28-11f1-a27a-00163e1435d4', 'UOS开发-1', '5.3.1', '588MB', 46545, 'https://download.uos.com/uos开发1.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c33748-1c28-11f1-a27a-00163e1435d4', 'UOS开发-2', '3.3.1', '504MB', 15916, 'https://download.uos.com/uos开发2.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c39d27-1c28-11f1-a27a-00163e1435d4', 'UOS开发-3', '2.8.5', '217MB', 35654, 'https://download.uos.com/uos开发3.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c4074c-1c28-11f1-a27a-00163e1435d4', 'UOS开发-4', '1.5.2', '512MB', 91047, 'https://download.uos.com/uos开发4.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c46c0f-1c28-11f1-a27a-00163e1435d4', 'UOS开发-5', '5.2.3', '26MB', 99695, 'https://download.uos.com/uos开发5.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c4d0a1-1c28-11f1-a27a-00163e1435d4', 'UOS开发-6', '5.4.6', '1005MB', 95082, 'https://download.uos.com/uos开发6.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c53430-1c28-11f1-a27a-00163e1435d4', 'UOS开发-7', '4.7.6', '976MB', 89388, 'https://download.uos.com/uos开发7.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c5a116-1c28-11f1-a27a-00163e1435d4', 'UOS开发-8', '3.9.2', '152MB', 12355, 'https://download.uos.com/uos开发8.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c606b0-1c28-11f1-a27a-00163e1435d4', 'UOS开发-9', '1.3.3', '771MB', 71749, 'https://download.uos.com/uos开发9.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c65563-1c28-11f1-a27a-00163e1435d4', 'UOS开发-10', '2.1.9', '377MB', 96611, 'https://download.uos.com/uos开发10.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c6ab90-1c28-11f1-a27a-00163e1435d4', 'UOS开发-11', '4.5.6', '440MB', 35224, 'https://download.uos.com/uos开发11.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c70fdb-1c28-11f1-a27a-00163e1435d4', 'UOS开发-12', '3.0.1', '375MB', 48138, 'https://download.uos.com/uos开发12.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92c77851-1c28-11f1-a27a-00163e1435d4', 'UOS开发-13', '2.8.6', '630MB', 14149, 'https://download.uos.com/uos开发13.exe', 'UOS软件研发部-开发工具组', 'UOS官方-UOS开', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d42b99-1c28-11f1-a27a-00163e1435d4', 'UOS系统-1', '4.5.5', '27MB', 42416, 'https://download.uos.com/uos系统1.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d496e1-1c28-11f1-a27a-00163e1435d4', 'UOS系统-2', '1.8.2', '526MB', 94273, 'https://download.uos.com/uos系统2.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d4ffdd-1c28-11f1-a27a-00163e1435d4', 'UOS系统-3', '1.7.5', '361MB', 15768, 'https://download.uos.com/uos系统3.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d56438-1c28-11f1-a27a-00163e1435d4', 'UOS系统-4', '4.9.8', '362MB', 18918, 'https://download.uos.com/uos系统4.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d5d180-1c28-11f1-a27a-00163e1435d4', 'UOS系统-5', '5.6.7', '965MB', 42429, 'https://download.uos.com/uos系统5.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d63728-1c28-11f1-a27a-00163e1435d4', 'UOS系统-6', '2.7.2', '89MB', 55519, 'https://download.uos.com/uos系统6.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d6e973-1c28-11f1-a27a-00163e1435d4', 'UOS系统-7', '3.8.5', '450MB', 49575, 'https://download.uos.com/uos系统7.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d74edd-1c28-11f1-a27a-00163e1435d4', 'UOS系统-8', '1.0.0', '42MB', 2036, 'https://download.uos.com/uos系统8.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d79c53-1c28-11f1-a27a-00163e1435d4', 'UOS系统-9', '5.7.8', '961MB', 26630, 'https://download.uos.com/uos系统9.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d7e965-1c28-11f1-a27a-00163e1435d4', 'UOS系统-10', '3.3.5', '642MB', 53741, 'https://download.uos.com/uos系统10.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d853e7-1c28-11f1-a27a-00163e1435d4', 'UOS系统-11', '4.1.3', '339MB', 66432, 'https://download.uos.com/uos系统11.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d8efad-1c28-11f1-a27a-00163e1435d4', 'UOS系统-12', '2.4.3', '638MB', 97044, 'https://download.uos.com/uos系统12.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92d9542b-1c28-11f1-a27a-00163e1435d4', 'UOS系统-13', '5.6.7', '580MB', 66787, 'https://download.uos.com/uos系统13.exe', 'UOS软件研发部-系统工具组', 'UOS官方-UOS系', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92e6e64a-1c28-11f1-a27a-00163e1435d4', 'UOS网络-1', '3.9.8', '515MB', 98288, 'https://download.uos.com/uos网络1.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92e7548a-1c28-11f1-a27a-00163e1435d4', 'UOS网络-2', '2.8.0', '879MB', 15368, 'https://download.uos.com/uos网络2.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92e7ba84-1c28-11f1-a27a-00163e1435d4', 'UOS网络-3', '1.1.2', '90MB', 54002, 'https://download.uos.com/uos网络3.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92e828b4-1c28-11f1-a27a-00163e1435d4', 'UOS网络-4', '3.4.0', '802MB', 88738, 'https://download.uos.com/uos网络4.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92e88d31-1c28-11f1-a27a-00163e1435d4', 'UOS网络-5', '1.4.0', '892MB', 35609, 'https://download.uos.com/uos网络5.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92e8f217-1c28-11f1-a27a-00163e1435d4', 'UOS网络-6', '1.3.6', '47MB', 29684, 'https://download.uos.com/uos网络6.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92e9611a-1c28-11f1-a27a-00163e1435d4', 'UOS网络-7', '2.7.7', '679MB', 100499, 'https://download.uos.com/uos网络7.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92e9c596-1c28-11f1-a27a-00163e1435d4', 'UOS网络-8', '5.8.3', '200MB', 91812, 'https://download.uos.com/uos网络8.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92ea2819-1c28-11f1-a27a-00163e1435d4', 'UOS网络-9', '5.1.7', '175MB', 71558, 'https://download.uos.com/uos网络9.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92ea8d2b-1c28-11f1-a27a-00163e1435d4', 'UOS网络-10', '1.0.1', '496MB', 7160, 'https://download.uos.com/uos网络10.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92eaf13e-1c28-11f1-a27a-00163e1435d4', 'UOS网络-11', '5.0.7', '534MB', 41508, 'https://download.uos.com/uos网络11.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92eb3d96-1c28-11f1-a27a-00163e1435d4', 'UOS网络-12', '3.0.8', '242MB', 54771, 'https://download.uos.com/uos网络12.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92eba5f7-1c28-11f1-a27a-00163e1435d4', 'UOS网络-13', '5.3.7', '810MB', 70361, 'https://download.uos.com/uos网络13.exe', 'UOS软件研发部-网络工具组', 'UOS官方-UOS网', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fb09cb-1c28-11f1-a27a-00163e1435d4', 'UOS教育-1', '1.2.0', '527MB', 43406, 'https://download.uos.com/uos教育1.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fb7b03-1c28-11f1-a27a-00163e1435d4', 'UOS教育-2', '3.5.1', '95MB', 95242, 'https://download.uos.com/uos教育2.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fbcdac-1c28-11f1-a27a-00163e1435d4', 'UOS教育-3', '3.4.9', '158MB', 4520, 'https://download.uos.com/uos教育3.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fc3605-1c28-11f1-a27a-00163e1435d4', 'UOS教育-4', '4.5.5', '125MB', 92949, 'https://download.uos.com/uos教育4.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fc861d-1c28-11f1-a27a-00163e1435d4', 'UOS教育-5', '2.4.7', '191MB', 71306, 'https://download.uos.com/uos教育5.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fcee70-1c28-11f1-a27a-00163e1435d4', 'UOS教育-6', '5.7.8', '809MB', 59096, 'https://download.uos.com/uos教育6.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fd4104-1c28-11f1-a27a-00163e1435d4', 'UOS教育-7', '3.7.4', '667MB', 9178, 'https://download.uos.com/uos教育7.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fda811-1c28-11f1-a27a-00163e1435d4', 'UOS教育-8', '3.9.3', '136MB', 47474, 'https://download.uos.com/uos教育8.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fdf893-1c28-11f1-a27a-00163e1435d4', 'UOS教育-9', '5.3.7', '10MB', 62840, 'https://download.uos.com/uos教育9.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92fe5f20-1c28-11f1-a27a-00163e1435d4', 'UOS教育-10', '1.5.6', '662MB', 21974, 'https://download.uos.com/uos教育10.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92feb0d6-1c28-11f1-a27a-00163e1435d4', 'UOS教育-11', '1.8.8', '733MB', 11580, 'https://download.uos.com/uos教育11.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92ff1f47-1c28-11f1-a27a-00163e1435d4', 'UOS教育-12', '2.4.2', '994MB', 9697, 'https://download.uos.com/uos教育12.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('92ff71fa-1c28-11f1-a27a-00163e1435d4', 'UOS教育-13', '3.1.2', '880MB', 58915, 'https://download.uos.com/uos教育13.exe', 'UOS软件研发部-教育学习组', 'UOS官方-UOS教', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('930f3111-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-1', '2.6.5', '769MB', 12227, 'https://download.uos.com/uos娱乐1.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('930f9dac-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-2', '2.0.5', '514MB', 88447, 'https://download.uos.com/uos娱乐2.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('93103692-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-3', '5.6.8', '1005MB', 57150, 'https://download.uos.com/uos娱乐3.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('93109cdf-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-4', '5.4.6', '938MB', 73947, 'https://download.uos.com/uos娱乐4.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('9311039d-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-5', '5.1.0', '725MB', 54188, 'https://download.uos.com/uos娱乐5.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('93116775-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-6', '3.9.3', '650MB', 28448, 'https://download.uos.com/uos娱乐6.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('9311db13-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-7', '3.4.7', '597MB', 63251, 'https://download.uos.com/uos娱乐7.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('93123ed3-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-8', '2.8.3', '123MB', 52455, 'https://download.uos.com/uos娱乐8.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('9312a7fd-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-9', '2.6.4', '194MB', 70118, 'https://download.uos.com/uos娱乐9.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('93130fee-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-10', '5.4.5', '205MB', 47341, 'https://download.uos.com/uos娱乐10.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('93135eb6-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-11', '4.2.1', '793MB', 58686, 'https://download.uos.com/uos娱乐11.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('9313abb3-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-12', '3.9.1', '730MB', 28277, 'https://download.uos.com/uos娱乐12.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);
INSERT INTO `software` VALUES ('931411e7-1c28-11f1-a27a-00163e1435d4', 'UOS娱乐-13', '2.1.3', '264MB', 17988, 'https://download.uos.com/uos娱乐13.exe', 'UOS软件研发部-娱乐休闲组', 'UOS官方-UOS娱', '2026-03-10 10:27:16', '2026-03-10 10:27:16', NULL);

-- ----------------------------
-- Table structure for system_info
-- ----------------------------
DROP TABLE IF EXISTS `system_info`;
CREATE TABLE `system_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NOT NULL COMMENT '软件名称',
  `major` int(11) NOT NULL DEFAULT 1 COMMENT '主版本号（如1）',
  `minor` int(11) NOT NULL DEFAULT 0 COMMENT '次版本号（如2）',
  `patch` int(11) NOT NULL DEFAULT 0 COMMENT '修订版本号（如3）',
  `author` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NULL DEFAULT '' COMMENT '作者',
  `update_log` text CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci NULL DEFAULT '' COMMENT '更新日志',
  `is_force` tinyint(4) NULL DEFAULT 0 COMMENT '是否强制更新（1=是，0=否）',
  `created_time` datetime NULL DEFAULT current_timestamp() COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT current_timestamp() ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_time` datetime NULL DEFAULT NULL COMMENT '删除时间（软删除）',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_uca1400_ai_ci COMMENT = '系统软件版本信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of system_info
-- ----------------------------
INSERT INTO `system_info` VALUES (1, 'UOS应用商店', 1, 1, 0, 'Admin', '1. 优化缓存逻辑；2. 新增自动更新功能', 0, '2026-03-10 10:03:01', '2026-03-10 10:03:01', NULL);

-- ----------------------------
-- Procedure structure for InsertSoftwareByCategory
-- ----------------------------
DROP PROCEDURE IF EXISTS `InsertSoftwareByCategory`;
delimiter ;;
CREATE PROCEDURE `InsertSoftwareByCategory`(IN p_category_name VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci,
    IN p_software_prefix VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci,
    IN p_start_num INT,
    IN p_end_num INT)
BEGIN
    DECLARE v_classify_id INT UNSIGNED;
    DECLARE v_current_num INT;
    DECLARE v_software_id CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci;
    DECLARE v_error_msg VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci;
    
    -- 获取分类ID（二进制比较兼容排序规则）
    SELECT id INTO v_classify_id 
    FROM classify 
    WHERE BINARY name = BINARY p_category_name 
      AND deleted_time IS NULL;
    
    -- 分类不存在则终止
    IF v_classify_id IS NULL THEN
        SET v_error_msg = CONCAT('分类【', p_category_name, '】不存在，终止插入');
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = v_error_msg;
    END IF;
    
    -- 循环插入软件
    SET v_current_num = p_start_num;
    WHILE v_current_num <= p_end_num DO
        SET v_software_id = UUID();
        
        INSERT INTO software (
            id, name, version, size, download_count, download_url, 
            provider_department, provider
        ) VALUES (
            v_software_id,
            CONCAT(p_software_prefix, v_current_num),
            CONCAT(FLOOR(RAND()*5)+1, '.', FLOOR(RAND()*10), '.', FLOOR(RAND()*10)),
            CONCAT(FLOOR(RAND()*1000)+10, 'MB'),
            FLOOR(RAND()*100000)+1000,
            CONCAT('https://download.uos.com/', LOWER(REPLACE(p_software_prefix, '-', '')), v_current_num, '.exe'),
            CONCAT('UOS软件研发部-', p_category_name, '组'),
            CONCAT('UOS官方-', SUBSTRING(p_software_prefix, 1, 4))
        );
        
        INSERT IGNORE INTO classify2software (classify_id, software_id)
        VALUES (v_classify_id, v_software_id);
        
        SET v_current_num = v_current_num + 1;
    END WHILE;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
