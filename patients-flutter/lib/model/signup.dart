import 'dart:convert';

class SignupForm {
  late String first_name;
  late String last_name;
  late String email;
  late String password;
  late int department_id;
  late String gender;
  late String role;


  SignupForm(
      {
        required this.first_name,
        required this.last_name,
        required this.email,
        required this.password,
        required this.department_id,
        required this.gender,
        required this.role,
      }
    );

  factory SignupForm.fromJson(Map<String, dynamic> map) {
    return SignupForm(
        first_name: map["first_name"],
        last_name: map["last_name"],
        email: map["email"],
        password: map["password"],
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
      "password": password,
      "department_id": department_id,
      "gender": gender,
      "role": role,
    };
  }

  @override
  String toString() {
    return 'SignupForm{'
        'first_name: $first_name,'
        ' last_name: $last_name,'
        ' email: $email,'
        ' password: $password,'
        ' department_id: $department_id,'
        ' gender: $gender,'
        ' role: $role'
        '}';
  }

}

List<SignupForm> SignupFormFromJson(String jsonData) {
  final data = json.decode(jsonData);
  return List<SignupForm>.from(data.map((item) => SignupForm.fromJson(item)));
}

String SignupFormToJson(SignupForm data) {
  final jsonData = data.toJson();
  return json.encode(jsonData);
}
