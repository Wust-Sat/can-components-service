import asyncio
import click

from can_logger.callbacks import format_message
from can_logger.can_interface import CANInterface
from can_logger.database import CANMessageDatabase
from life_guard.life_center import LifeGuard
from life_guard.life_center import Device

async def async_main(interface, db_path):
    can_interface = CANInterface(interface)
    db_interface = CANMessageDatabase(db_path)

    #############################
    lg = LifeGuard()
    dev1=Device(node_id=1, name="Bat")
    dev2=Device(node_id=2, name="EPS1")
    dev3=Device(node_id=3, name="EPS2")
    lg.add_device(dev1)
    lg.add_device(dev2)
    lg.add_device(dev3)
    await lg.start()
    ###############################

    await can_interface.connect()
    db_interface.connect()

    async def monitorX(message):
        # print(lg.monitor(message))
        lg.monitor(message)

    def db_message_handler(message):
        db_interface.add_message(message)

    can_interface.add_receive_callback(db_message_handler)
    can_interface.add_receive_callback(monitorX)



    try:
        while can_interface.running:
            await can_interface.receive_frame(timeout=1.0)

    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        await can_interface.disconnect()
        db_interface.disconnect()


@click.command()
@click.option(
    "-i",
    "--interface",
    required=True,
    type=str,
    help="CAN interface name (e.g., vcan0, can0).",
)
@click.option(
    "-d",
    "--db-path",
    type=str,
    default="can_messages.db",
    help="Path to SQLite database file for saving messages.",
)
def main(interface, db_path):
    asyncio.run(async_main(interface, db_path))


if __name__ == "__main__":
    main()
