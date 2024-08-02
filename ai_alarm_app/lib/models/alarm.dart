class Alarm {
  final String time;
  final bool isSnoozed;

  Alarm({required this.time, this.isSnoozed = false});

  factory Alarm.fromJson(Map<String, dynamic> json) {
    return Alarm(
      time: json['current_time'],
      isSnoozed: json['snoozed'],
    );
  }
}