import 'dart:convert';

import 'dart:ffi';

class PatientForm {
    var id;
   var first_name;
   var last_name;
   var email;
   var description;
   var med_list;
   var age;
   var link;
   var image;
   var phone_number;
   var date_of_birth;
   var street_address;
   var city_address;
   var zipcode_address;
   var state_address;
   var gender;
   var emergency_contact_name;
   var emergency_phone_number;
   var relationship;
   var is_in_hospital;
   var user;
   var tags;
   var treatment;
   var image_lists;
   var creation_date;
   var modified_date;

  PatientForm(
      {
        this.id,
        required this.first_name,
        required this.last_name,
        this.description,
        this.med_list,
        required this.age,
        this.link,
        this.image,
        this.phone_number,
        this.date_of_birth,
        this.street_address,
        this.city_address,
        this.zipcode_address,
        this.state_address,
        this.gender,
        this.emergency_contact_name,
        this.emergency_phone_number,
        this.relationship,
        this.is_in_hospital,
        this.user,
        required this.tags,
        required this.treatment,
        required this.image_lists,
        this.creation_date,
        this.modified_date,
      }
 );

  factory PatientForm.fromJson(Map<String, dynamic> map) {
    return PatientForm(
        id: map["id"],
        first_name: map["first_name"],
        last_name: map["last_name"],
        description: map["description"],
        med_list: map["med_list"],
        age: map["age"],
        link: map["link"],
        image: map["image"],
        phone_number: map["phone_number"],
        date_of_birth: map["date_of_birth"],
        street_address: map["street_address"],
        city_address: map["city_address"],
        zipcode_address: map["zipcode_address"],
        state_address: map["state_address"],
        creation_date: map["creation_date"],
        modified_date: map["modified_date"],
        gender: map["gender"],
        emergency_contact_name: map["emergency_contact_name"],
        emergency_phone_number: map["emergency_phone_number"],
        relationship: map["relationship"],
        is_in_hospital: map["is_in_hospital"],
        user: map["user"],
        tags: map["tags"],
        treatment: map["treatment"],
        image_lists: map["image_lists"]
    );
  }

  Map<String, dynamic> toJson() {
    return {
      "id": id,
      "first_name": first_name,
      "last_name": last_name,
      "description": description,
      "med_list": med_list,
      "age": age,
      "link": link,
      "image": image,
      "phone_number": phone_number,
      "date_of_birth": date_of_birth,
      "street_address": street_address,
      "city_address": city_address,
      "zipcode_address": zipcode_address,
      "state_address": state_address,
      "creation_date": creation_date,
      "modified_date": modified_date,
      "gender": gender,
      "emergency_contact_name": emergency_contact_name,
      "emergency_phone_number": emergency_phone_number,
      "relationship": relationship,
      "is_in_hospital": is_in_hospital,
      'user': user,
      "tags": tags,
      "treatment": treatment,
      "image_lists": image_lists
    };
  }

  // @override
  // String toString() {
  //   return 'PatientForm{'
  //       'first_name: $first_name,'
  //       ' last_name: $last_name,'
  //       ' email: $email,'
  //       ' department_id: $department_id,'
  //       ' gender: $gender,'
  //       ' role: $role'
  //       '}';
  // }

}

List<PatientForm> PatientFormFromJson(String jsonData) {
  final data = json.decode(jsonData);
  return List<PatientForm>.from(data.map((item) => PatientForm.fromJson(item)));
}

String PatientFormToJson(PatientForm data) {
  final jsonData = data.toJson();
  return json.encode(jsonData);
}
