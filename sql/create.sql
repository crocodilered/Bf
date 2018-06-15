-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               10.1.22-MariaDB - mariadb.org binary distribution
-- Операционная система:         Win64
-- HeidiSQL Версия:              9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Дамп структуры базы данных bf
CREATE DATABASE IF NOT EXISTS `bf` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `bf`;

-- Дамп структуры для таблица bf.calculation
CREATE TABLE IF NOT EXISTS `calculation` (
  `calculation_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text,
  `params_template` text,
  `updated` timestamp DEFAULT CURRENT_TIMESTAMP COMMENT 'Копия graph.updated',
  PRIMARY KEY (`calculation_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COMMENT='Тип рассчета';

-- Дамп данных таблицы bf.calculation: ~2 rows (приблизительно)
/*!40000 ALTER TABLE `calculation` DISABLE KEYS */;
INSERT INTO `calculation` (`calculation_id`, `title`, `description`, `params_template`, `updated`) VALUES
	(1, 'Количество итераций', 'Рассчет зависимости количества итераций от числа нейронов.', '{\r\n"side_size": 7,\r\n"n_samples": 100,\r\n"pos_prob": 0.1,\r\n"noise": "10, 12",\r\n"population_size": 200,\r\n"to_survive": 0.1,\r\n"mut_lim": 1,\r\n"n_neurons": "65, 100, 5",\r\n"condition": 0.02,\r\n"l1": 1E-4,\r\n"l2": 1E-5\r\n}', '2018-05-30 15:04:23');
/*!40000 ALTER TABLE `calculation` ENABLE KEYS */;

-- Дамп структуры для таблица bf.data
CREATE TABLE IF NOT EXISTS `data` (
  `data_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `graph_id` int(11) NOT NULL,
  `x` double NOT NULL,
  `y` double NOT NULL,
  `created` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`data_id`),
  KEY `graph_id` (`graph_id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COMMENT='Данные для графиков.';

-- Дамп данных таблицы bf.data: ~8 rows (приблизительно)
/*!40000 ALTER TABLE `data` DISABLE KEYS */;
INSERT INTO `data` (`data_id`, `graph_id`, `x`, `y`, `created`) VALUES
	(73, 44, 65, 54, '2018-05-30 13:20:50'),
	(74, 44, 70, 66, '2018-05-30 13:27:15'),
	(75, 44, 75, 49, '2018-05-30 13:31:43'),
	(76, 44, 80, 42, '2018-05-30 13:35:24'),
	(77, 44, 85, 100, '2018-05-30 14:28:06'),
	(78, 44, 90, 59, '2018-05-30 14:34:35'),
	(79, 44, 95, 104, '2018-05-30 14:47:36'),
	(80, 44, 100, 99, '2018-05-30 15:04:23');
/*!40000 ALTER TABLE `data` ENABLE KEYS */;

-- Дамп структуры для таблица bf.graph
CREATE TABLE IF NOT EXISTS `graph` (
  `graph_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `calculation_id` int(11) NOT NULL,
  `params` text NOT NULL,
  `finished` tinyint(4) DEFAULT '0',
  `created` timestamp,
  `updated` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`graph_id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COMMENT='Список графиков';

-- Дамп данных таблицы bf.graph: ~1 rows (приблизительно)
/*!40000 ALTER TABLE `graph` DISABLE KEYS */;
INSERT INTO `graph` (`graph_id`, `title`, `calculation_id`, `params`, `finished`, `created`, `updated`) VALUES
	(44, 'Прямо тест тест', 2, '{"side_size": "7", "n_samples": "100", "pos_prob": "0.1", "noise": "10, 12", "population_size": "200", "to_survive": "0.1", "mut_lim": "1", "n_neurons": "65, 100, 5", "condition": "0.02", "l1": "0.0001", "l2": "1e-05"}', 1, '2018-05-30 13:16:45', '2018-05-30 15:22:16');
/*!40000 ALTER TABLE `graph` ENABLE KEYS */;

-- Дамп структуры для таблица bf.user
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(250) NOT NULL DEFAULT '',
  `password` varchar(250) NOT NULL DEFAULT '',
  `enabled` tinyint(4) NOT NULL DEFAULT '1',
  `token` varchar(36) DEFAULT NULL,
  `created` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  KEY `token` (`token`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Дамп данных таблицы bf.user: ~1 rows (приблизительно)
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`user_id`, `email`, `password`, `enabled`, `token`, `created`) VALUES
	(1, 'user@corp.com', '$2b$12$3jiCgvlBI6MmdQe4lozqvOsQVTkCVeeMaGPKvKAQxsaQqHjWjZFv6', 1, NULL, '2018-05-24 17:09:54');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
