import 'package:flutter/material.dart';
import '../services/alarm_service.dart';

class SetAlarmScreen extends StatefulWidget {
  const SetAlarmScreen({Key? key}) : super(key: key);

  @override
  _SetAlarmScreenState createState() => _SetAlarmScreenState();
}

class _SetAlarmScreenState extends State<SetAlarmScreen> {
  final AlarmService _alarmService = AlarmService();
  TimeOfDay _bedTime = TimeOfDay.now();
  TimeOfDay _wakeUpTime = TimeOfDay.now();

  Future<void> _selectTime(BuildContext context, bool isBedTime) async {
    final TimeOfDay? picked = await showTimePicker(
      context: context,
      initialTime: isBedTime ? _bedTime : _wakeUpTime,
    );
    if (picked != null) {
      setState(() {
        if (isBedTime) {
          _bedTime = picked;
        } else {
          _wakeUpTime = picked;
        }
      });
    }
  }

  String _formatTimeOfDay(TimeOfDay timeOfDay) {
    final now = DateTime.now();
    final dateTime = DateTime(now.year, now.month, now.day, timeOfDay.hour, timeOfDay.minute);
    return "${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}";
  }

  Future<void> _setAlarm() async {
    try {
      final result = await _alarmService.setAlarm(
        _formatTimeOfDay(_bedTime),
        _formatTimeOfDay(_wakeUpTime),
      );
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Alarm set for ${result['optimal_time']}')),
      );
      Navigator.pop(context);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to set alarm: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Set Alarm'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Bed Time: ${_formatTimeOfDay(_bedTime)}'),
            ElevatedButton(
              onPressed: () => _selectTime(context, true),
              child: const Text('Select Bed Time'),
            ),
            const SizedBox(height: 20),
            Text('Wake Up Time: ${_formatTimeOfDay(_wakeUpTime)}'),
            ElevatedButton(
              onPressed: () => _selectTime(context, false),
              child: const Text('Select Wake Up Time'),
            ),
            const SizedBox(height: 40),
            Center(
              child: ElevatedButton(
                onPressed: _setAlarm,
                child: const Text('Set Alarm'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}