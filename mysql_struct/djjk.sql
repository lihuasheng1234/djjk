
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `load_data`;
CREATE TABLE `load_data`  (
  `data` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '更新时间',
  `machine_num` int(11) NOT NULL,
  UNIQUE INDEX `machine_num`(`machine_num`) USING BTREE,
  CONSTRAINT `machine_num` FOREIGN KEY (`machine_num`) REFERENCES `machine_info` (`machine_num`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;


INSERT INTO `load_data` VALUES ('[2, 1, 2, 1, 1]', '2021-04-13 10:25:43', 1);


DROP TABLE IF EXISTS `machine_info`;
CREATE TABLE `machine_info`  (
  `machine_num` int(11) NOT NULL,
  `machine_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `machine_class` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`machine_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

INSERT INTO `machine_info` VALUES (1, 'Fanuc', '加工中心');
INSERT INTO `machine_info` VALUES (2, 'Fanuc2', '加工中心2');


DROP TABLE IF EXISTS `tool_hp`;
CREATE TABLE `tool_hp`  (
  `hp` double(255, 4) NULL DEFAULT NULL,
  `tool_num` int(11) NOT NULL,
  `machine_num` int(11) NULL DEFAULT NULL,
  `time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  INDEX `hp_machine`(`machine_num`) USING BTREE,
  INDEX `hp_tool`(`tool_num`) USING BTREE,
  CONSTRAINT `hp_machine` FOREIGN KEY (`machine_num`) REFERENCES `machine_info` (`machine_num`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `hp_tool` FOREIGN KEY (`tool_num`) REFERENCES `tool_info` (`tool_num`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

INSERT INTO `tool_hp` VALUES (0.7809, 2, 1, '2021-04-13 10:25:37');
INSERT INTO `tool_hp` VALUES (0.7809, 2, 1, '2021-04-13 10:25:40');


DROP TABLE IF EXISTS `tool_info`;
CREATE TABLE `tool_info`  (
  `tool_num` int(11) NULL DEFAULT NULL,
  `djgg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `djpp` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `jgjs` int(255) NULL DEFAULT NULL,
  `machine_num` int(11) NULL DEFAULT NULL,
  INDEX `machine_info`(`machine_num`) USING BTREE,
  INDEX `tool_num`(`tool_num`) USING BTREE,
  CONSTRAINT `machine_info` FOREIGN KEY (`machine_num`) REFERENCES `machine_info` (`machine_num`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;


INSERT INTO `tool_info` VALUES (1, 'MX7-01', 'Fii', 1, 1);
INSERT INTO `tool_info` VALUES (2, 'MX7-01', 'Fii', 2, 1);
INSERT INTO `tool_info` VALUES (1, 'MX7-01', 'Fii', 3, 2);
INSERT INTO `tool_info` VALUES (2, 'MX7-01', 'Fii', 4, 2);
INSERT INTO `tool_info` VALUES (3, 'MX7-01', 'Fii', 5, 2);


DROP TABLE IF EXISTS `vib_data`;
CREATE TABLE `vib_data`  (
  `data` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0),
  `machine_num` int(11) NULL DEFAULT NULL,
  INDEX `sensor_machine_num`(`machine_num`) USING BTREE,
  CONSTRAINT `sensor_machine_num` FOREIGN KEY (`machine_num`) REFERENCES `machine_info` (`machine_num`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;


INSERT INTO `vib_data` VALUES ('600,-240,-163,213,-23,-487,-231,360,488,-394,-109,282,-232,-460,-438,-245,-163,595,417,569,-212,-189,305,-329,-122,92,355,-534,327,-408,-96,-271,202,-153,-207,-301,279,-168,-422,431,29,378,-86,-10,-506,-384,413,-232,351,197,-15,84,-87,272,370,-260,398,-142,-260,-223,419', '2021-04-13 10:25:43', 1);


DROP TABLE IF EXISTS `warming`;
CREATE TABLE `warming`  (
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `time` datetime(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  `machine_num` int(11) NULL DEFAULT NULL,
  `tool_num` int(11) NULL DEFAULT NULL,
  `djgg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  INDEX `warming_machine`(`machine_num`) USING BTREE,
  CONSTRAINT `warming_machine` FOREIGN KEY (`machine_num`) REFERENCES `machine_info` (`machine_num`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;


INSERT INTO `warming` VALUES ('dd', '2021-03-26 15:22:06', 1, 7, '\r\nMX7-07');
INSERT INTO `warming` VALUES ('ms', '2021-02-20 14:00:30', 1, 7, 'MX7-07');
INSERT INTO `warming` VALUES ('qa', '2021-03-29 14:13:29', 1, 7, 'MX7-07');
INSERT INTO `warming` VALUES ('qaa', '2020-03-29 14:13:44', 1, 7, 'MX7-07');

SET FOREIGN_KEY_CHECKS = 1;
