import 'package:flutter/material.dart';
import '../services/alarm_service.dart';
import '../widgets/alarm_tile.dart';
import '../models/alarm.dart';

class AlarmListScreen extends StatefulWidget {
  @override
  _AlarmListScreenState createState() => _AlarmListScreenState();
}

class _AlarmListScreenState extends State<AlarmListScreen> {
  final AlarmService _alarmService = AlarmService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Alarms'),
      ),
      body: FutureBuilder(
        future: _alarmService.getAlarms(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else {
            final alarms = snapshot.data as List<Alarm>;
            return ListView.builder(
              itemCount: alarms.length,
              itemBuilder: (context, index) {
                return AlarmTile(alarm: alarms[index]);
              },
            );
          }
        },
      ),
    );
  }
}