

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


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

SET FOREIGN_KEY_CHECKS = 1;
