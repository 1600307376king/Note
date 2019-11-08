/*
Navicat MySQL Data Transfer

Source Server         : local
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : note

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2019-11-08 17:30:44
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for notes
-- ----------------------------
DROP TABLE IF EXISTS `notes`;
CREATE TABLE `notes` (
  `n_id` int(11) NOT NULL,
  `note_title` varchar(255) DEFAULT NULL,
  `note_labels` varchar(255) DEFAULT NULL,
  `note_content` text DEFAULT NULL,
  `note_instructions` text DEFAULT NULL,
  `creation_time` datetime DEFAULT NULL,
  PRIMARY KEY (`n_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of notes
-- ----------------------------
INSERT INTO `notes` VALUES ('0', '【数据结构】之线性表（顺序存储结构）', '数据结构|计算机原理|', '1\n## 一、数组实现方式\n2\n​\n3\n#####线性表的数据结构，其中 MAX 表示线性表的数组元素个数，就是线性表的最大容量，length 表示线性表当前的长度。这里有一个必要条件，就是 length <= MAX\n4\n​\n5\n    #define MAX 20\n6\n    typedef int ElemType;\n7\n    typedef struct\n8\n    {\n9\n        ElemType data[MAX]; \n10\n        int length;\n11\n    }SqList;\n12\n​\n', ' 线性表是《数据结构》课程最开始的一章的内容，是在大学计算机专业必学的课程。我们刚接触线性表时，可能会被它的几种表的结构搞得晕头转向，它有两种基本存储结构：一种是顺序存储结构，另一种是链式存储结构。接下来，我们先来看看线性表的顺序存储结构吧。\n                    ', '2019-11-08 16:28:49');
