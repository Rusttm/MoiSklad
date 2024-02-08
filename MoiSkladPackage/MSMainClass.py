from MSPkgLogger import MSPkgLogger


class MSMainClass(MSPkgLogger):
    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = MSMainClass()
    connect.logger.info("testing MainClass")
