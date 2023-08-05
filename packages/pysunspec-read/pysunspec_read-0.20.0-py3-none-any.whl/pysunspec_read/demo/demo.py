import logging
from pathlib import Path

from pysunspec_read.connect_options import ConnectOptions, ConnectOptionsTcp
from pysunspec_read.demo.init_logging import setup_logging
from pysunspec_read.output_options import OutputOptions
from pysunspec_read.read_to_output import read_with_clean

base_dir = "C:/solar_monitor/test/app/"
setup_logging(base_dir + "logging.yaml")

logger = logging.getLogger(__name__)
logger.info("****************************")
logger.info("*         Starting         *")
logger.info("****************************")


def run():
    print("Starting")
    output = Path("C:/solar_monitor/adhoc_output/demo.json")
    read_with_clean(connect_options=ConnectOptions(tcp=ConnectOptionsTcp(ip_address="192.168.1.110")),
                    output_options=OutputOptions(output_file_path=output, add_timestamp_to_reading=True))


if __name__ == '__main__':
    run()
