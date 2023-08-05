#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
This Mentat module is a real-time message processing daemon capable of converting IDEA (https://idea.cesnet.cz/)
messages to MISP core format (https://datatracker.ietf.org/doc/draft-dulaunoy-misp-core-format/) and inserting them to
MISP instance.

This daemon is implemented using the :py:mod:`pyzenkit.zendaemon` framework and
so it provides all of its core features. See the documentation for in-depth
details.

It is further based on :py:mod:`mentat.daemon.piper` module, which provides
*pipe-like* message processing features. See the documentation for in-depth
details.
"""

import mentat.const
import mentat.daemon.piper
import mentat.daemon.component.parser
import mentat.daemon.component.commiter

from mentat_misp_connector.component_misper import MisperDaemonComponent


class MentatMisperDaemon(mentat.daemon.piper.PiperDaemon):
    """
    Daemon component capable of converting IDEA (https://idea.cesnet.cz/) messages to MISP core format
    (https://datatracker.ietf.org/doc/draft-dulaunoy-misp-core-format/) and inserting them to MISP instance.
    """

    def __init__(self):
        """
        Initialize misper daemon object. This method overrides the base
        implementation in :py:func:`pyzenkit.zendaemon.ZenDaemon.__init__` and
        it aims to even more simplify the daemon object creation by providing
        configuration values for parent contructor.
        """
        super().__init__(
            description = 'mentat-misper.py - IDEA to MISP converting daemon',
            #
            # Define required daemon components.
            #
            components = [
                mentat.daemon.component.parser.ParserDaemonComponent(),
                mentat.daemon.component.misper.MisperDaemonComponent()
            ]
        )

    def _init_argparser(self, **kwargs):
        """
        Initialize daemon command line argument parser. This method overrides the
        base implementation in :py:func:`mentat.daemon.piper.PiperDaemon._init_argparser`
        and it must return valid :py:class:`argparse.ArgumentParser` object. It
        appends additional command line options custom for this daemon object.

        This method is called from the main constructor in :py:func:`pyzenkit.baseapp.BaseApp.__init__`
        as a part of the **__init__** stage of application`s life cycle.

        :param kwargs: Various additional parameters passed down from object constructor.
        :return: Valid argument parser object.
        :rtype: argparse.ArgumentParser
        """
        argparser = super()._init_argparser(**kwargs)
        return argparser

    def _init_config(self, cfgs, **kwargs):
        """
        Initialize default daemon configurations. This method overrides the base
        implementation in :py:func:`mentat.daemon.piper.PiperDaemon._init_config`
        and it appends additional configurations via ``cfgs`` parameter.

        This method is called from the main constructor in :py:func:`pyzenkit.baseapp.BaseApp.__init__`
        as a part of the **__init__** stage of application`s life cycle.

        :param list cfgs: Additional set of configurations.
        :param kwargs: Various additional parameters passed down from constructor.
        :return: Default configuration structure.
        :rtype: dict
        """
        cfgs = (
            (mentat.daemon.component.misper.CONFIG_MISP_URL, ""),
            (mentat.daemon.component.misper.CONFIG_MISP_KEY, ""),
            (mentat.daemon.component.misper.CONFIG_MISP_CERT, "")
        ) + cfgs
        return super()._init_config(cfgs, **kwargs)

