# -*- coding: utf-8 -*-

import logging
class Logger:
    def __init__(self,file="run.log"):
        """[summary]
        快速

        Args:
            file (str, optional): [description]. 日志文件目录位置
        """
        
        logger = logging.getLogger()

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Setup file handler
        fhandler  = logging.FileHandler(file)
        fhandler.setLevel(logging.DEBUG)
        fhandler.setFormatter(formatter)

#         # Configure stream handler for the cells
        chandler = logging.StreamHandler()
        chandler.setLevel(logging.DEBUG)
        chandler.setFormatter(formatter)

#         # Add both handlers
        logger.addHandler(fhandler)
        logger.addHandler(chandler)
        logger.setLevel(logging.DEBUG)

        # Show the handlers
        logger.handlers
        self.logger=logger
    def add(self,text):
        """[summary]
        添加日志信息，默认采用info

        Args:
            text ([type]): [description] 日志内容
        """
        # Log Something
        self.logger.info(text)

    def info(self,text):
        """[summary]
        添加info日志信息

        Args:
            text ([type]): [description]
        """
        # Log Something
        self.logger.info(text)
    def debug(self,text):
        """[summary]
        添加debug日志信息

        Args:
            text ([type]): [description]
        """
        # Log Something
        self.logger.debug(text)
    def error(self,text):
        """[summary]
        添加error日志信息

        Args:
            text ([type]): [description]
        """
        # Log Something
        self.logger.error(text)        

# ————————————————
# 版权声明：本文为CSDN博主「农民小飞侠」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/w5688414/article/details/100882268
# logger=tkitLogger()
# logger.add("dd")