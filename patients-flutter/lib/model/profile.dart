import 'dart:convert';

class ProfileForm {
  late String first_name;
  late String last_name;
  late String email;
  late int department_id;
  late String gender;
  late String role;


  ProfileForm(
      {
        required this.first_name,
        required this.last_name,
        required this.email,
        required this.department_id,
        required this.gender,
        required this.role,
      }
      );

  factory ProfileForm.fromJson(Map<String, dynamic> map) {
    return ProfileForm(
      first_name: map["first_name"],
      last_name: map["last_name"],
      email: map["email"],
      department_id: map["department_id"],
      gender: map["gender"],
      role: map["role"],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "first_name": first_name,
      "last_name": last_name,
      "email": email,
      "department_id": department_id,
      "gender": gender,
      "role": role,
    };
  }

  @override
  String toString() {
    return 'ProfileForm{'
        'first_name: $first_name,'
        ' last_name: $last_name,'
        ' email: $email,'
        ' department_id: $department_id,'
        ' gender: $gender,'
        ' role: $role'
        '}';
  }

}

List<ProfileForm> ProfileFormFromJson(String jsonData) {
  final data = json.decode(jsonData);
  return List<ProfileForm>.from(data.map((item) => ProfileForm.fromJson(item)));
}

String ProfileFormToJson(ProfileForm data) {
  final jsonData = data.toJson();
  return json.encode(jsonData);
}
