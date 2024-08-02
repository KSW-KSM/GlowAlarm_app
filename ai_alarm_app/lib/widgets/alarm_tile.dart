import 'package:flutter/material.dart';
import '../models/alarm.dart';

class AlarmTile extends StatelessWidget {
  final Alarm alarm;

  const AlarmTile({Key? key, required this.alarm}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(alarm.time),
      trailing: Icon(
        alarm.isSnoozed ? Icons.snooze : Icons.alarm,
        color: alarm.isSnoozed ? Colors.orange : Colors.blue,
      ),
    );
  }
}