#  ctx = Context()
#         rds = ctx.create_redis()
#         g = init(rds)
#
# # unpause telemd
#         ctx['telemd'].start_telemd()
#
#         # start exp
#         logger.info("Start experiment and wait for 1 second")
#         exp = g['exp']
#         exp.start(
#             name=config.exp_name,
#             creator=config.creator,
#             metadata=metadata
#         )
#         requests()
#
#         logger.info("Pause telemd")
#         ctx['telemd'].stop_telemd()
#         logger.info("Stop exp")
#         exp.stop()
