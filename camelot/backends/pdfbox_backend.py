# -*- coding: utf-8 -*-

import cv2
import glob
import logging
import numpy as np
import os
import subprocess

logger = logging.getLogger("camelot")
logger.setLevel(logging.INFO)

class PdfboxBackend(object):
    def __init__(self, pdfbox_app_path):
        self.pdfbox_app_path = pdfbox_app_path

        if not self.pdfbox_app_path:
            raise ValueError("pdfbox backend needs the path to pdfbox-app-x.y.z.jar")
        
        if not os.path.exists(self.pdfbox_app_path):
            raise ValueError(f"invalid pdfbox backend: {self.pdfbox_app_path}")
        
        logger.info(f"PdfboxBackend - pdfbox_app_path = {self.pdfbox_app_path}")

    
    def convert(self, pdf_path, png_path):
        logger.info(f"PdfboxBackend - pdf_path = {pdf_path}")
        logger.info(f"PdfboxBackend - png_path = {png_path}")

        pdftopng_command = ["java", "-jar", self.pdfbox_app_path, "PDFToImage", "-imageType", "png", "-dpi", "128", pdf_path]

        try:
            cmd = " ".join(pdftopng_command)
            logger.info(f"PdfboxBackend - conversion cmd = {cmd}")

            output = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=True
            )

            logger.info(f"PdfboxBackend - conversion output = {output}")

            # get the png file and rename it to png_path
            images = glob.glob(pdf_path.replace(".pdf", "*.png"))

            logger.info("PdfboxBackend - images = " + (' '.join(images)))

            # # evidentiaza tabelul
            # im = cv2.imread(images[0])
            
            # lower = np.array([192, 192, 192], dtype = "uint8")
            # upper = np.array([192, 192, 192], dtype = "uint8")
            
            # mask = cv2.inRange(im, lower, upper)
            # output = cv2.bitwise_and(im, im, mask = mask)

            # cv2.imshow("im", output)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            # cv2.imwrite(images[0], output)

            if len(images) == 1:
                os.rename(images[0], png_path)
            else:
                raise ValueError(f"There should be only 1 png file. Found {len(images)}")

        except subprocess.CalledProcessError as e:
            raise ValueError(e.output)
