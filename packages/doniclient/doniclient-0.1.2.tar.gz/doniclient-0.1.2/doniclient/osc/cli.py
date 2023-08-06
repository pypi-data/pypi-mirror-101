"""Implements Doni command line interface."""

import logging
from argparse import ArgumentTypeError
from typing import List

from dateutil import parser, tz
from keystoneauth1.exceptions import HttpError
from osc_lib import utils
from osc_lib.cli import parseractions
from osc_lib.command import command

LOG = logging.getLogger(__name__)  # Get the logger of this module


class DoniClientError(BaseException):
    """Base Error Class for Doni Client."""


class HardwareAction(command.Command):
    """Base class for create and update."""

    def __init__(self, app, app_args, cmd_name):
        super().__init__(app, app_args, cmd_name=cmd_name)

    optional_args = [
        "ipmi_username",
        "ipmi_password",
        "ipmi_terminal_port",
    ]

    columns = (
        "name",
        "project_id",
        "hardware_type",
        "properties",
        "uuid",
    )

    def parse_uuid(self, parser):
        """Get uuid to use as path."""
        parser.add_argument(
            dest="uuid", metavar="<uuid>", help=("unique ID of hw item")
        )

    def parse_mgmt_args(self, parser, required: bool = True):
        parser.add_argument(
            "--name",
            metavar="<name>",
            help=(
                "Name of the hardware object. Best practice is to use a "
                "universally unique identifier, such has serial number or chassis ID. "
                "This will aid in disambiguating systems."
            ),
            required=required,
        )
        parser.add_argument(
            "--hardware_type",
            metavar="<hardware_type>",
            help=("hardware_type of item"),
            required=required,
        )
        parser.add_argument("--mgmt_addr", metavar="<mgmt_addr>", required=required)
        parser.add_argument("--ipmi_username", metavar="<ipmi_username>")
        parser.add_argument("--ipmi_password", metavar="<ipmi_password>")
        parser.add_argument(
            "--ipmi_terminal_port", metavar="<ipmi_terminal_port>", type=int
        )

    def parse_interfaces(self, parser):
        parser.add_argument(
            "--iface_add",
            required_keys=["name", "mac"],
            action=parseractions.MultiKeyValueAction,
            help=(
                "Specify once per interface, in the form:\n `--interface name=<name>,mac=<mac_address>`"
            ),
        )
        parser.add_argument(
            "--iface_update",
            required_keys=["name", "mac", "index"],
            action=parseractions.MultiKeyValueAction,
            help=(
                "Specify once per interface, in the form:\n `--interface name=<name>,mac=<mac_address>,index=<index>`"
            ),
        )
        parser.add_argument(
            "--iface_delete",
            metavar="index",
            help=("Specify interface to delete, by index`"),
        )

    def parse_availability(self, parser):

        parser.add_argument(
            "--aw_add",
            action="append",
            nargs=2,
            metavar=("start", "end"),
            help="specify ISO compatible date for start and end of availability window",
        )
        parser.add_argument(
            "--aw_update",
            action="append",
            nargs=3,
            metavar=("id", "start", "end"),
            help=("Specify window to update by ID, then start and end dates"),
        )
        parser.add_argument(
            "--aw_delete",
            metavar="id",
            type=int,
            action="append",
            help=("Specify window to delete by ID"),
        )

    def get_parser(self, prog_name):
        """Add arguments to cli parser."""
        parser = super().get_parser(prog_name)
        parser.add_argument("--dry_run", action="store_true")

        self.parse_interfaces(parser)
        self.parse_availability(parser)

        return parser

    def _valid_date(self, s):
        LOG.debug(f"Processing Date {s}")
        try:
            parsed_dt = parser.parse(s)
            dt_with_tz = parsed_dt.replace(tzinfo=parsed_dt.tzinfo or tz.gettz())
            LOG.debug(dt_with_tz)
            return dt_with_tz
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise ArgumentTypeError(msg)

    def _format_iface(self, interface_args: List):
        interface_list = []
        key_map = {
            "name": "name",
            "mac_address": "mac",
        }
        for interface in interface_args or []:
            iface = {doni: interface.get(cmdline) for doni, cmdline in key_map}
            interface_list.append(iface)

        return interface_list

    def _format_window(self, window_args):
        result = {}
        result["start"] = self._valid_date(window_args[0])
        result["end"] = self._valid_date(window_args[1])
        return result

    def _format_window_id(self, window_args):
        result = {}
        result["index"] = int(window_args[0])
        result["start"] = self._valid_date(window_args[1])
        result["end"] = self._valid_date(window_args[2])
        return result


class ListHardware(command.Lister):
    """List all hardware in the Doni database."""

    columns = HardwareAction.columns

    def take_action(self, parsed_args):
        """List all hw items in Doni."""
        hw_client = self.app.client_manager.inventory
        try:
            data = hw_client.list()
        except HttpError as ex:
            LOG.error(ex.response.text)
            raise ex

        data_iterator = (
            utils.get_dict_properties(s, self.columns, formatters={}) for s in data
        )
        return (self.columns, data_iterator)


class ExportHardware(ListHardware):
    """Export public fields from the hw db."""

    columns = HardwareAction.columns

    def take_action(self, parsed_args):
        """Export Public hw items in Doni."""
        hw_client = self.app.client_manager.inventory
        try:
            data = hw_client.export()
        except HttpError as ex:
            LOG.error(ex.response.text)
            raise ex

        data_iterator = (
            utils.get_dict_properties(s, self.columns, formatters={}) for s in data
        )
        return (self.columns, data_iterator)


class GetHardware(command.ShowOne):
    """List specific hardware item in Doni."""

    columns = HardwareAction.columns

    def get_parser(self, prog_name):
        """Add arguments to cli parser."""
        parser = super().get_parser(prog_name)
        HardwareAction.parse_uuid(parser)
        return parser

    def take_action(self, parsed_args):
        """List all hw items in Doni."""
        hw_client = self.app.client_manager.inventory
        try:
            data = hw_client.get_by_uuid(parsed_args.uuid)
        except HttpError as ex:
            LOG.error(ex.response.text)
            raise ex

        return (
            self.columns,
            utils.get_dict_properties(data, self.columns, formatters={}),
        )


class DeleteHardware(command.Command):
    """Delete specific hardware item in Doni."""

    def get_parser(self, prog_name):
        """Add arguments to cli parser."""
        parser = super().get_parser(prog_name)
        HardwareAction.parse_uuid(self, parser)
        return parser

    def take_action(self, parsed_args):
        hw_client = self.app.client_manager.inventory
        try:
            result = hw_client.delete(parsed_args.uuid)
        except HttpError as ex:
            LOG.error(ex.response.text)
            raise ex

        return result.text


class SyncHardware(command.Command):
    """Sync specific hardware item in Doni."""

    def get_parser(self, prog_name):
        """Add arguments to cli parser."""
        parser = super().get_parser(prog_name)
        HardwareAction.parse_uuid(self, parser)
        return parser

    def take_action(self, parsed_args):
        hw_client = self.app.client_manager.inventory
        try:
            result = hw_client.sync(parsed_args.uuid)
        except HttpError as ex:
            LOG.error(ex.response.text)
            raise ex

        return result.text


class CreateHardware(HardwareAction):
    """Create a Hardware Object in Doni."""

    def __init__(self, app, app_args, cmd_name):
        super().__init__(app, app_args, cmd_name=cmd_name)

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        self.parse_mgmt_args(parser, required=True)
        return parser

    def take_action(self, parsed_args):
        """List all hw items in Doni."""
        hw_client = self.app.client_manager.inventory

        properties = {}
        properties["management_address"] = parsed_args.mgmt_addr
        properties["interfaces"] = self._format_iface(parsed_args.iface_add)

        # Set optional arguments
        for arg in self.optional_args:
            properties[arg] = getattr(parsed_args, arg)

        body = {
            "name": parsed_args.name,
            "hardware_type": parsed_args.hardware_type,
            "properties": properties,
        }

        if parsed_args.dry_run:
            LOG.warn(body)
        else:
            try:
                data = hw_client.create(body)
            except HttpError as ex:
                LOG.error(ex.response.text)
                raise ex

            return data.text


class UpdateHardware(HardwareAction):
    """Send JSON Patch to update resource."""

    def __init__(self, app, app_args, cmd_name):
        super().__init__(app, app_args, cmd_name=cmd_name)

    def get_parser(self, prog_name):
        """Add arguments to cli parser."""
        parser = super().get_parser(prog_name)
        self.parse_uuid(parser)
        self.parse_mgmt_args(parser, required=False)
        return parser

    def take_action(self, parsed_args):
        hw_client = self.app.client_manager.inventory
        uuid = parsed_args.uuid
        LOG.debug(parsed_args)
        patch = []
        field_map = {
            "name": "name",
            "hardware_type": "hardware_type",
            "management_address": "properties/management_address",
            "ipmi_username": "properties/ipmi_username",
            "ipmi_password": "properties/ipmi_password",
            "ipmi_terminal_port": "properties/ipmi_terminal_port",
        }

        for key, val in field_map.items():
            arg = getattr(parsed_args, key, None)
            if arg:
                patch.append({"op": "add", "path": f"/{val}", "value": arg})

        # Update Interfaces
        for iface in self._format_iface(getattr(parsed_args, "iface_add")):
            patch.append({"op": "add", "path": f"/interface/-", "value": iface})

        for iface in self._format_iface(getattr(parsed_args, "iface_update")):
            index = iface.pop("index")
            patch.append(
                {"op": "replace", "path": f"/interface/{index}", "value": iface}
            )
        for iface in getattr(parsed_args, "iface_delete") or []:
            index = iface.get("index")
            patch.append({"op": "remove", "path": f"/interface/{index}"})

        # Update Availability Windows
        for aw in getattr(parsed_args, "aw_add") or []:
            window = self._format_window(aw)
            patch.append({"op": "add", "path": f"/availability/-", "value": window})

        for aw in getattr(parsed_args, "aw_update") or []:
            LOG.debug(aw)
            window = self._format_window_id(aw)
            index = window.pop("index")
            patch.append(
                {"op": "replace", "path": f"/availability/{index}", "value": window}
            )
        for index in getattr(parsed_args, "aw_delete") or []:
            patch.append(
                {"op": "remove", "path": f"/availability/{index}", "value": aw}
            )

        if patch:
            try:
                LOG.debug(f"PATCH_BODY:{patch}")
                data = hw_client.update(uuid, patch)
            except HttpError as ex:
                LOG.error(ex.response.text)
                raise ex
            else:
                return data.text
        else:
            LOG.warn("No updates to send")
