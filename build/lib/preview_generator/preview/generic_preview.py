# -*- coding: utf-8 -*-

from io import BytesIO

import logging
import os
import typing

from preview_generator import file_converter
from preview_generator.exception import UnavailablePreviewType
from preview_generator.utils import ImgDims


class PreviewBuilderMeta(type):
    def __new__(
            mcs,
            *args,
            **kwargs
    ):
        cls = super(mcs).__new__(mcs, *args, **kwargs)
        cls = typing.cast(typing.Type['PreviewBuilder'], cls)
        return cls


class PreviewBuilder(object):
    __metaclass__ = PreviewBuilderMeta
    def __init__(
            self,
    ):
        logging.info('New Preview builder of class' + str(self.__class__))

    @classmethod
    def get_supported_mimetypes(cls):
        raise NotImplementedError()

    @classmethod
    def check_dependencies(cls):
        return True

    def get_page_number(
            self,
            file_path,
            preview_name,
            cache_path
    ):
        """
        Get the number of page of the document
        """
        raise UnavailablePreviewType()

    def build_jpeg_preview(
            self,
            file_path,
            preview_name,
            cache_path,
            page_id,
            extension = '.jpg',
            size=None
    ):
        """
        generate the jpg preview
        """
        raise UnavailablePreviewType()

    def has_pdf_preview(self):
        """
        Override and return True if your builder allow PDF preview
        :return:
        """
        return False

    def build_pdf_preview(
            self,
            file_path,
            preview_name,
            cache_path,
            extension = '.pdf',
            page_id = -1
    ):
        """
        generate the jpeg preview
        """
        raise UnavailablePreviewType()

    def build_html_preview(
            self,
            file_path,
            preview_name,
            cache_path,
            extension = '.html'
    ):
        """
        generate the html preview
        """
        raise UnavailablePreviewType()

    def build_json_preview(
            self,
            file_path,
            preview_name,
            cache_path,
            page_id = 0,
            extension = '.json'
    ):
        """
        generate the json preview
        """
        raise UnavailablePreviewType()

    def build_text_preview(
            self,
            file_path,
            preview_name,
            cache_path,
            page_id = 0,
            extension = '.txt'
    ):
        """
        return file content from the cache
        """
        raise UnavailablePreviewType()


class OnePagePreviewBuilder(PreviewBuilder):
    """
    Generic preview handler for single page document
    """

    def get_page_number(
            self,
            file_path,
            preview_name,
            cache_path
    ):
        return 1


class ImagePreviewBuilder(OnePagePreviewBuilder):
    """
    Generic preview handler for an Image (except multi-pages images)
    """

    def _get_json_stream_from_image_stream(
        self,
            img,
            filesize=0
    ):
        return file_converter.image_to_json(img, filesize)

    def build_json_preview(
            self,
            file_path,
            preview_name,
            cache_path,
            page_id = 0,
            extension = '.json'
    ):
        """
        generate the json preview
        """

        with open(file_path, 'rb') as img:
            filesize = os.path.getsize(file_path)
            json_stream = self._get_json_stream_from_image_stream(img, filesize)
            with open(cache_path + preview_name + extension, 'wb') as jsonfile:
                buffer = json_stream.read(256)
                while buffer:
                    jsonfile.write(buffer)
                    buffer = json_stream.read(256)
