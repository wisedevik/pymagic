Interceptor.attach(
  Module.findExportByName("libg.so", "_ZN8Debugger7warningEPKc"),
  {
    onEnter(args) {
      console.log(`[warning] ${args[0].readUtf8String()}`);
    },
  },
);

Interceptor.attach(
  Module.findExportByName("libg.so", "_ZN8Debugger5errorEPKc"),
  {
    onEnter(args) {
      console.log(`[error] ${args[0].readUtf8String()}`);
    },
  },
);

Interceptor.attach(
  Module.findExportByName("libg.so", "_ZN8Debugger8hudPrintEPKc"),
  {
    onEnter(args) {
      console.log(`[hud] ${args[0].readUtf8String()}`);
    },
  },
);

Interceptor.attach(
  Module.findExportByName(
    "libg.so",
    "_ZN14MessageManager14receiveMessageEP14PiranhaMessage",
  ),
  {
    onEnter(args) {
      let message = args[1];
      let messageType = new NativeFunction(
        Memory.readPointer(Memory.readPointer(message).add(20)),
        "int",
        ["pointer"],
      )(message);
      console.log(
        "[MessageManager::receiveMessage] Received " + messageType,
        +" length=" +
          new NativeFunction(
            Module.findExportByName("libg.so", "_ZNK10ByteStream9getLengthEv"),
            "int",
            ["pointer"],
          )(message),
      );
    },
  },
);
