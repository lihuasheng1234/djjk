
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


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

SET FOREIGN_KEY_CHECKS = 1;
