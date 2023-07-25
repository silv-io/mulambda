# import time
#
# from galileo.shell.shell import init
# from galileo.worker.context import Context
#
#
# def main():
#     ctx = Context()
#     rds = ctx.create_redis()
#     g = init(rds)
#     exp = g["exp"]
#     telemd = g["telemd"]
#
#     print("Unpausing telemd...")
#     telemd.start_telemd()
#     print("Starting test experiment...")
#     exp.start(name="test", creator="silvio", metadata={"test": "test"})
#     print("Sleeping for 3 seconds...")
#     time.sleep(3)
#
#     print("Pausing telemd...")
#     telemd.stop_telemd()
#     print("Stopping experiment...")
#     exp.stop()
#     print("Experiment finished.")
#
#
# if __name__ == "__main__":
#     main()
