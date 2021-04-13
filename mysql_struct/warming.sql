
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

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
