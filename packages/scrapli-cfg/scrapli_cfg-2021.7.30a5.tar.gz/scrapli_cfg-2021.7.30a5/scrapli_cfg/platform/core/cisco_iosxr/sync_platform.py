"""scrapli_cfg.platform.core.cisco_iosxr.sync_platform"""
from typing import Any, Callable, List, Optional

from scrapli.driver import NetworkDriver
from scrapli_cfg.diff import ScrapliCfgDiffResponse
from scrapli_cfg.exceptions import DiffConfigError, LoadConfigError
from scrapli_cfg.platform.base.sync_platform import ScrapliCfgPlatform
from scrapli_cfg.platform.core.cisco_iosxr.base_platform import CONFIG_SOURCES, ScrapliCfgIOSXRBase
from scrapli_cfg.response import ScrapliCfgResponse


def iosxr_on_open(cls: ScrapliCfgPlatform) -> None:
    """
    Scrapli CFG IOSXR On open

    Disable console logging, perhaps more things in the future!

    Args:
        cls: ScrapliCfg object

    Returns:
        None

    Raises:
        N/A

    """
    cls.conn.send_configs(configs=["no logging console", "commit"])


class ScrapliCfgIOSXR(ScrapliCfgPlatform, ScrapliCfgIOSXRBase):
    def __init__(
        self,
        conn: NetworkDriver,
        config_sources: Optional[List[str]] = None,
        on_open: Optional[Callable[..., Any]] = None,
        preserve_connection: bool = False,
    ) -> None:
        if config_sources is None:
            config_sources = CONFIG_SOURCES

        if on_open is None:
            on_open = iosxr_on_open

        super().__init__(
            conn=conn,
            config_sources=config_sources,
            on_open=on_open,
            preserve_connection=preserve_connection,
        )

        self._replace = False

        self._in_configuration_session = False
        self._config_privilege_level = "configuration"

    def get_version(self) -> ScrapliCfgResponse:
        response = self._pre_get_version()

        version_result = self.conn.send_command(command="show version | i Version")

        return self._post_get_version(
            response=response,
            scrapli_responses=[version_result],
            result=self._parse_version(device_output=version_result.result),
        )

    def get_config(self, source: str = "running") -> ScrapliCfgResponse:
        response = self._pre_get_config(source=source)

        if not self._in_configuration_session:
            config_result = self.conn.send_command(command="show running-config")
        else:
            config_result = self.conn.send_config(
                config="show running-config", privilege_level=self._config_privilege_level
            )

        return self._post_get_config(
            response=response,
            source=source,
            scrapli_responses=[config_result],
            result=config_result.result,
        )

    def load_config(self, config: str, replace: bool = False, **kwargs: Any) -> ScrapliCfgResponse:
        """
        Load configuration to a device

        Supported kwargs:
            exclusive: True/False use `configure exclusive` mode

        Args:
            config: string of the configuration to load
            replace: replace the configuration or not, if false configuration will be loaded as a
                merge operation
            kwargs: additional kwargs that the implementing classes may need for their platform,
                see above for iosxr supported kwargs

        Returns:
            ScrapliCfgResponse: response object

        Raises:
            N/A

        """
        scrapli_responses = []
        response = self._pre_load_config(config=config)

        exclusive = kwargs.get("exclusive", False)

        config, eager_config = self._prepare_load_config_session_and_payload(
            config=config, replace=replace, exclusive=exclusive
        )

        try:
            config_result = self.conn.send_config(
                config=config, privilege_level=self._config_privilege_level
            )
            scrapli_responses.append(config_result)
            if config_result.failed:
                msg = "failed to load the candidate config into the config session"
                self.logger.critical(msg)
                raise LoadConfigError(msg)

            # eager cuz banners and such; perhaps if no banner/macro we can disable eager though....
            if eager_config:
                eager_config_result = self.conn.send_config(
                    config=eager_config, privilege_level=self._config_privilege_level, eager=True
                )
                scrapli_responses.append(eager_config_result)
                if eager_config_result.failed:
                    msg = "failed to load the candidate config into the config session"
                    self.logger.critical(msg)
                    raise LoadConfigError(msg)

        except LoadConfigError:
            pass

        return self._post_load_config(
            response=response,
            scrapli_responses=scrapli_responses,
        )

    def abort_config(self) -> ScrapliCfgResponse:
        response = self._pre_abort_config(session_or_config_file=self._in_configuration_session)

        self.conn._abort_config()  # pylint: disable=W0212
        self._reset_config_session()

        return self._post_abort_config(response=response, scrapli_responses=[])

    def commit_config(self, source: str = "running") -> ScrapliCfgResponse:
        response = self._pre_commit_config(
            source=source, session_or_config_file=self._in_configuration_session
        )

        commit_result = self.conn.send_config(config="commit")
        self._reset_config_session()

        return self._post_commit_config(response=response, scrapli_responses=[commit_result])

    def diff_config(self, source: str = "running") -> ScrapliCfgDiffResponse:
        scrapli_responses = []
        device_diff = ""
        source_config = ""

        diff_response = self._pre_diff_config(
            source=source, session_or_config_file=self._in_configuration_session
        )

        try:
            diff_result = self.conn.send_config(
                config=self._get_diff_command(), privilege_level=self._config_privilege_level
            )
            scrapli_responses.append(diff_result)
            if diff_result.failed:
                msg = "failed generating diff for config session"
                self.logger.critical(msg)
                raise DiffConfigError(msg)

            device_diff = diff_result.result

            source_config_result = self.get_config(source=source)
            source_config = source_config_result.result

            if source_config_result.scrapli_responses:
                scrapli_responses.extend(source_config_result.scrapli_responses)

            if source_config_result.failed:
                msg = "failed fetching source config for diff comparison"
                self.logger.critical(msg)
                raise DiffConfigError(msg)

        except DiffConfigError:
            pass

        source_config, candidate_config = self._normalize_source_candidate_configs(
            source_config=source_config
        )

        return self._post_diff_config(
            diff_response=diff_response,
            scrapli_responses=scrapli_responses,
            source_config=source_config,
            candidate_config=candidate_config,
            device_diff=device_diff,
        )
