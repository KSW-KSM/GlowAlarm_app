import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/alarm.dart';

class AlarmService {
  final String baseUrl = 'http://localhost:8000'; // 서버 URL을 적절히 변경하세요

    Future<Map<String, dynamic>> setAlarm(String bedTime, String wakeUpTime) async {
    final response = await http.post(
      Uri.parse('$baseUrl/set_alarm'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'bed_time': bedTime,
        'wake_up_time': wakeUpTime,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to set alarm: ${response.body}');
    }
  }

  Future<List<Alarm>> getAlarms() async {
    final response = await http.get(Uri.parse('$baseUrl/alarms'));

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body);
      return data.entries.map((e) => Alarm.fromJson(e.value)).toList();
    } else {
      throw Exception('Failed to load alarms');
    }
  }
}

class AlarmResponse {
  final String message;
  final String optimalTime;

  AlarmResponse({required this.message, required this.optimalTime});

  factory AlarmResponse.fromJson(Map<String, dynamic> json) {
    return AlarmResponse(
      message: json['message'],
      optimalTime: json['optimal_time'],
    );
  }
}