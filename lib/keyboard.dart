import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:onscreen_num_keyboard/onscreen_num_keyboard.dart';

class MyKeyboardPage extends StatefulWidget {
  const MyKeyboardPage({super.key});

  @override
  State<MyKeyboardPage> createState() => _MyKeyboardPageState();
}

class _MyKeyboardPageState extends State<MyKeyboardPage>{
  String text = "";

  _onKeyboardTap(String value) {
    setState(() {
      text = text + value;
    });
  }

  @override
  Widget build(BuildContext context) {
    // This method is rerun every time setState is called, for instance as done
    // by the _incrementCounter method above.
    //
    // The Flutter framework has been optimized to make rerunning build methods
    // fast, so that you can just rebuild anything that needs updating rather
    // than having to individually change instances of widgets.
    return Scaffold(
      appBar: AppBar(
        // TRY THIS: Try changing the color here to a specific color (to
        // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
        // change color while the other colors stay the same.
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        // Here we take the value from the MyHomePage object that was created by
        // the App.build method, and use it to set our appbar title.
        title: const Text("Keyboard"),
      ),
      body: NumericKeyboard(
          onKeyboardTap: _onKeyboardTap,
          textStyle: const TextStyle(
              fontSize: 20.0,
              color: Colors.black
          ),
          rightButtonFn: () {
            if (text.isEmpty) return;
            setState(() {
              text = text.substring(0, text.length - 1);
            });
          },
          rightButtonLongPressFn: () {
            if (text.isEmpty) return;
            setState(() {
              text = '';
            });
          },
          rightIcon: const Icon(Icons.backspace, color: Colors.red,),
          leftButtonFn: () {
            log('left button clicked');
          },
          leftIcon: const Icon(Icons.check, color: Colors.red,),
          mainAxisAlignment: MainAxisAlignment.spaceEvenly
      )
    );
  }
}
