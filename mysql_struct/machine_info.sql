
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


DROP TABLE IF EXISTS `machine_info`;
CREATE TABLE `machine_info`  (
  `machine_num` int(11) NOT NULL,
  `machine_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `machine_class` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`machine_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

INSERT INTO `machine_info` VALUES (1, 'Fanuc', '加工中心');
INSERT INTO `machine_info` VALUES (2, 'Fanuc2', '加工中心2');

SET FOREIGN_KEY_CHECKS = 1;
