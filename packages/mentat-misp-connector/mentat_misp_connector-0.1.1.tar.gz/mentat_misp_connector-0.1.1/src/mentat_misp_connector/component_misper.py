#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Daemon component capable of converting IDEA (https://idea.cesnet.cz/) messages to MISP core format
(https://datatracker.ietf.org/doc/draft-dulaunoy-misp-core-format/) and inserting them to MISP instance.

The implementation is based on :py:class:`pyzenkit.zendaemon.ZenDaemonComponent`.

"""

import re
import json
from datetime import datetime

from pymisp import logger as pymisp_logger
from pymisp import ExpandedPyMISP, MISPEvent, MISPObject

import pyzenkit.zendaemon


CONFIG_MISP_URL = "misp_url"
CONFIG_MISP_KEY = "misp_key"
CONFIG_MISP_CERT = "misp_cert"


class MisperDaemonComponent(pyzenkit.zendaemon.ZenDaemonComponent):
    """
    Daemon component capable of converting IDEA (https://idea.cesnet.cz/) messages to MISP core format
    (https://datatracker.ietf.org/doc/draft-dulaunoy-misp-core-format/) and inserting them to MISP instance.
    """
    EVENT_START = 'start'
    EVENT_STOP = 'stop'

    EVENT_MSG_PROCESS = 'message_process'
    EVENT_LOG_STATISTICS = 'log_statistics'

    STATS_CNT_CONVERTED = 'cnt_converted'
    STATS_CNT_ERRORS = 'cnt_errors'
    STATS_CNT_PUSHED = 'cnt_success_pushed'

    def __init__(self, **kwargs):
        """
        Perform component initializations.
        """
        super().__init__(**kwargs)

        # Unique component identifier
        self.cid = kwargs.get('cid', 'misper')

        self.misp_url = None
        self.misp_key = None
        self.misp_cert = None
        self.misp_inst = None
        # TODO remove, just for debug purposes
        self.daemon = None
        self.counter = 0

    def setup(self, daemon):
        """
        Perform component setup.
        """
        self.misp_key = daemon.c(CONFIG_MISP_KEY)
        self.misp_url = daemon.c(CONFIG_MISP_URL)
        self.misp_cert = daemon.c(CONFIG_MISP_CERT)

        daemon.logger.info(f"Loaded arguments: key: {self.misp_key}, url: {self.misp_url}, cert: {self.misp_cert}!")

        self.misp_inst = ExpandedPyMISP(self.misp_url, self.misp_key, True if self.misp_cert == "" else self.misp_cert)
        daemon.logger.debug("MISP instance version: {}".format(self.misp_inst.misp_instance_version))

    def get_events(self):
        """
        Get the list of event names and their appropriate callback handlers.
        """
        return [
            {
                'event': self.EVENT_START,
                'callback': self.cbk_event_start,
                'prepend': False
            },
            {
                'event': self.EVENT_STOP,
                'callback': self.cbk_event_stop,
                'prepend': False
            },
            {
                'event': self.EVENT_MSG_PROCESS,
                'callback': self.cbk_event_message_process,
                'prepend': False
            },
            {
                'event': self.EVENT_LOG_STATISTICS,
                'callback': self.cbk_event_log_statistics,
                'prepend': False
            }
        ]

    #---------------------------------------------------------------------------

    def cbk_event_start(self, daemon, args):
        """
        Start the component.
        """
        daemon.logger.debug(f"Component '{self.cid}': Starting the component")
        return (daemon.FLAG_CONTINUE, args)

    def cbk_event_stop(self, daemon, args):
        """
        Stop the component.
        """
        daemon.logger.debug(f"Component '{self.cid}': Stopping the component")
        return (daemon.FLAG_CONTINUE, args)

    def convert_event_and_push(self, daemon, idea_event):
        """
        Convert idea event and push it to MISP instance
        :param daemon: daemon instance
        :param idea_event: event, which will get converted
        :return: None
        """
        converted_event = self.converter.to_misp(idea_event, test=self.test)
        self.inc_statistic(self.STATS_CNT_CONVERTED)
        response = self.misp_inst.add_event(converted_event)
        if isinstance(response, MISPEvent):
            self.inc_statistic(self.STATS_CNT_PUSHED)
            daemon.logger.info("IDEA event {idea_id} was successfully converted and added to MISP instance under "
                               "id {misp_id}!".format(idea_id=idea_event['ID'], misp_id=response.id))
        elif isinstance(response, dict) and not response.get('errors'):
            self.inc_statistic(self.STATS_CNT_PUSHED)
            daemon.logger.info("IDEA event {idea_id} was successfully converted and added to MISP instance under "
                               "id {misp_id}!".format(idea_id=idea_event['ID'], misp_id=response['Event']['id']))
        else:
            self.inc_statistic(self.STATS_CNT_ERRORS)
            daemon.logger.error(
                "IDEA event {idea_id} was not pushed to MISP instance, because something went wrong "
                "MISP server side! Response error message follows:\n{errors}".format(idea_id=idea_event['ID'],
                                                                                     errors=response['errors']))

    def _can_be_processed(self, idea_event: dict) -> bool:
        """
        Every message has to contain three attributes, if it wants to be processed: source IP, dest IP and dest port.
        One combination is enough, but at least one is necessary.
        :param idea_event: tested idea event
        :return: True or False based on presence of three attributes
        """
        try:
            _ = idea_event['Source'][0]["IP4"]
            _ = idea_event['Target'][0]["IP4"]
            _ = idea_event['Target'][0]["Port"]
            return True
        except (KeyError, IndexError) as e:
            self.daemon.logger.info(e)
            return False

    def _get_all_attributes_from_idea(self, idea_event: dict):
        """ Get all source ips, destination ips and ports from idea event. """
        src_ips = []
        for source in idea_event.get('Source', []):
            for ip in source.get('IP4', []):
                src_ips.append(ip)
        dst_ips, dst_ports = [], []
        for target in idea_event.get('Target', []):
            for ip in target.get('IP4', []):
                dst_ips.append(ip)
            for port in target.get('Port', []):
                dst_ports.append(str(port))
        return src_ips, dst_ips, dst_ports

    def _get_all_three_tuples_from_idea(self, idea_event):
        """ Get all possible combinations of src ips, dst ips and dst ports. """
        src_ips, dst_ips, dst_ports = self._get_all_attributes_from_idea(idea_event)
        if not all((src_ips, dst_ips, dst_ports)):
            self.daemon.logger.info(f"Not enough attributes to create at least one three tuple, skip this message!")
        self.daemon.logger.info(f"src ips: {src_ips}\ndst_ips: {dst_ips}\ndst_ports: {dst_ports}")
        new_objects_all_combinations = set()
        for src_ip in src_ips:
            for dst_ip in dst_ips:
                for dst_port in dst_ports:
                    new_objects_all_combinations.add((src_ip, dst_ip, dst_port))
        return new_objects_all_combinations

    def _get_unique_id_for_three_tuple(self, three_tuple):
        """ Calculate unique id - WAIT FOR ALGORITHM DESCRIPTION """
        self.counter += 1
        return str(self.counter)

    def _get_all_unique_object_attributes(self, idea_event):
        """ For every three tuple in IDEA event calculate unique identifier and return it with tuples. """
        all_three_tuples = self._get_all_three_tuples_from_idea(idea_event)
        self.daemon.logger.info(f"All three tuples: {all_three_tuples}")
        unique_ids_with_values = {}
        for three_tuple in all_three_tuples:
            unique_id = self._get_unique_id_for_three_tuple(three_tuple)
            self.daemon.logger.info(f"Unique id for three tuple {three_tuple} is {unique_id}!")
            unique_ids_with_values[unique_id] = three_tuple
        return unique_ids_with_values

    def _add_sighting_to_existing_attr(self, obj: MISPObject):
        """ Adds positive sighting to source ip of passed object. """
        for attr in obj.Attribute:
            if attr.object_relation == "ip-src":
                sighting = attr.add_sighting({"id": attr.id, 'type': 0})
                resp = self.misp_inst.add_sighting(sighting, attr)
                if "Sighting" not in resp:
                    self.daemon.logger.error(f"Could not add sighting to object {obj.id}, because {resp}!")
                    return False
                return True
        return False

    def _add_sightings_to_present_objects(self, three_tuples: dict, misp_event: MISPEvent) -> int:
        """ Add sighting to all available objects identified by unique id. """
        updated_count = 0
        for obj in misp_event.objects:
            # self.da
            obj_unique_id = obj.comment
            if obj_unique_id in three_tuples.keys():
                added_flag = self._add_sighting_to_existing_attr(obj)
                if added_flag:
                    updated_count += 1
        return updated_count

    def _create_new_misp_object(self, values: tuple, unique_id: str, misp_event):
        """ Creates new MISP object with sighting on src ip. """
        attrs = {
            'ip-src': values[0],
            'ip-dst': values[1],
            'dst-port': values[2]
        }
        misp_obj = MISPObject(name="ip-port", strict=True)
        for attr_name, value in attrs.items():
            misp_obj.add_attribute(object_relation=attr_name, value=value)
        misp_obj.comment = unique_id
        res = self.misp_inst.add_object(misp_event, misp_obj, pythonify=True)
        self._add_sighting_to_existing_attr(res)

    def _process_idea_event(self, idea_event):
        """ Find all three tuples of src ips, dst ips and dst ports, try to update sightings in MISP of those, which
         already exist in MISP or if the three tuple is only one, create the object if it does not exist already. """
        self.daemon.logger.info("working")
        if not self._can_be_processed(idea_event):
            self.daemon.logger.info("Cannot process")
            return None
        all_new_objects = self._get_all_unique_object_attributes(idea_event)
        misp_intelmq_ev = self.misp_inst.get_event(10282, pythonify=True)
        self.daemon.logger.info(f"Calculated new objects: {all_new_objects}")
        updated_objects_total = self._add_sightings_to_present_objects(all_new_objects, misp_intelmq_ev)
        if updated_objects_total == 0 and len(all_new_objects) == 0:
            # create new object
            three_tuple_to_create = list(all_new_objects.values())[0]
            self._create_new_misp_object(three_tuple_to_create,
                                         self._get_unique_id_for_three_tuple(three_tuple_to_create),
                                         misp_intelmq_ev)
            self.misp_inst.publish(misp_intelmq_ev.id)

    def cbk_event_message_process(self, daemon, args):
        """
        Store the message into the persistent storage.
        """
        self.daemon = daemon
        # convert to raw json, without datetimes - for now, later can be updated
        daemon.logger.info("Received new idea event!")
        daemon.logger.info(type(args['idea']))
        idea_event_str = json.dumps(args['idea'], default=args['idea'].json_default)
        idea_event = json.loads(idea_event_str)
        daemon.logger.info("Idea message: {}".format(idea_event))
        self._process_idea_event(idea_event)
        # self._publish_event()
        self.daemon = None
        return (daemon.FLAG_CONTINUE, args)

    def cbk_event_log_statistics(self, daemon, args):
        """
        Periodical processing statistics logging.
        """
        stats = self.get_statistics()
        stats_str = ''

        for k in [self.STATS_CNT_CONVERTED, self.STATS_CNT_PUSHED, self.STATS_CNT_ERRORS]:
            if k in stats:
                stats_str = self.pattern_stats.format(stats_str, k, stats[k]['cnt'], stats[k]['inc'], stats[k]['spd'])
            else:
                stats_str = self.pattern_stats.format(stats_str, k, 0, 0, 0)

        daemon.logger.info(
            "Component '{}': *** Processing statistics ***{}".format(
                self.cid,
                stats_str
            )
        )
        return (daemon.FLAG_CONTINUE, args)
