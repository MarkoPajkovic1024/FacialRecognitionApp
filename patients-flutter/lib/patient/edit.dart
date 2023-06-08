import 'dart:convert';
import 'dart:io';

import 'package:date_time_picker/date_time_picker.dart';
import 'package:doctor/api/api.dart';
import 'package:doctor/model/patient.dart';
import 'package:doctor/patient/patient.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'package:textfield_tags/textfield_tags.dart';

class EditPatient extends StatefulWidget {
  const EditPatient({Key? key, required this.title, required this.patient, required this.type}) : super(key: key);

  final String title;
  final String type;
  final dynamic patient;

  @override
  State<EditPatient> createState() => _EditPatientState();
}

class _EditPatientState extends State<EditPatient> {
  bool _isLoading = false;
  final TextEditingController _controllerFirstName = TextEditingController();
  final TextEditingController _controllerLastName = TextEditingController();
  final TextEditingController _controllerDescription = TextEditingController();
  final TextEditingController _controllerMedList = TextEditingController();
  final TextEditingController _controllerAge = TextEditingController();
  final TextEditingController _controllerLink = TextEditingController();
  final TextEditingController _controllerImage = TextEditingController();
  final TextEditingController _controllerPhoneNumber = TextEditingController();
  late String _controllerDateOfBirth = "2000-08-01";
  final TextEditingController _controllerStreetAddress = TextEditingController();
  final TextEditingController _controllerCityAddress = TextEditingController();
  final TextEditingController _controllerZipcodeAddress = TextEditingController();
  final TextEditingController _controllerStateAddress = TextEditingController();
  late  String _controllerGender = "Male";
  final TextEditingController _controllerEmergencyContactMe = TextEditingController();
  final TextEditingController _controllerEmergencyPhoneNumber = TextEditingController();
  late String _controllerRelationship = "Spouse";
  late String _controllerIsInHospital = "Yes";
  final TextEditingController _controllerUser = TextEditingController();
  late TextfieldTagsController _controllerTreatment = TextfieldTagsController();
  late TextfieldTagsController _controllerTags = TextfieldTagsController();
  late TextfieldTagsController _controllerImageLists = TextfieldTagsController();

  List<String> _controllerInitTags = [];
  List<String> _controllerInitTreatment = [];

  late String _messageFirstName = "";
  late String _messageLastName = "";
  late String _messageDescription = "";
  late String _messageMedList = "";
  late String _messageAge = "";
  late String _messageImage = "";
  late String _messageLink = "";
  late String _messagePhoneNumber = "";
  late String _messageDateOfBirth = "";
  late String _messageStreetAddress = "";
  late String _messageCityAddress = "";
  late String _messageZipcodeAddress = "";
  late String _messageStateAddress = "";
  late String _messageGender = "";
  late String _messageEmergencyContactMe = "";
  late String _messageEmergencyPhoneNumber = "";
  late String _messageRelationship = "";
  late String _messageIsInHospital = "";
  late String _messageUser = "";
  late String _messageTags = "";
  late String _messageTreatment = "";
  late String _messageImageLists = "";

  List<DropdownMenuItem<String>> get _genderItems{
    List<DropdownMenuItem<String>> menuItems = [
      const DropdownMenuItem(child: Text("Male"),value: "Male"),
      const DropdownMenuItem(child: Text("Female"),value: "Female"),
      const DropdownMenuItem(child: Text("Non-binary/non-conforming"),value: "Non-binary/non-conforming"),
      const DropdownMenuItem(child: Text("Prefer not to respond"),value: "Prefer not to respond"),
    ];
    return menuItems;
  }

  List<DropdownMenuItem<String>> get _relationshipItems{
    List<DropdownMenuItem<String>> menuItems = [
      const DropdownMenuItem(child: Text("Spouse"),value: "Spouse"),
      const DropdownMenuItem(child: Text("Mother"),value: "Mother"),
      const DropdownMenuItem(child: Text("Father"),value: "Father"),
      const DropdownMenuItem(child: Text("Children"),value: "Children"),
      const DropdownMenuItem(child: Text("Friend"),value: "Friend"),
      const DropdownMenuItem(child: Text("Not Applicable"),value: "Not Applicable"),
    ];
    return menuItems;
  }

  List<DropdownMenuItem<String>> get _isInHospitalItems{
    List<DropdownMenuItem<String>> menuItems = [
      const DropdownMenuItem(child: Text("Yes"),value: "Yes"),
      const DropdownMenuItem(child: Text("No"),value: "No"),
    ];
    return menuItems;
  }
  
  ApiService _apiService = ApiService();

  //Open Image
  List<XFile>? imageFileList = [];
  final ImagePicker imgpicker = ImagePicker();
  bool multiFlag = false;

  void chooseImages() async {
    final choosedimages = await imgpicker.pickMultiImage();
    if (choosedimages != null) {
      imageFileList = choosedimages;
      setState((){
        multiFlag = true;
      });
    }
  }

  // chooseCameras() async {
  //   final choosedimage = await imgpicker.pickMultiImage(source: ImageCourse.camera);
  //   if(choosedimage != null){
  //     setState(() {
  //       multiFlag = true;
  //       imageFileList!.add(choosedimage);
  //     });
  //   }
  // }

  //Tags
  late double _distanceToField;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _distanceToField = MediaQuery.of(context).size.width;
  }

  @override
  void dispose() {
    super.dispose();
    _controllerTags.dispose();
    _controllerTreatment.dispose();
    _controllerImageLists.dispose();
  }

  @override
  void initState() {
      _controllerFirstName.text = jsonDecode(widget.patient)["first_name"] ?? "";
      _controllerLastName.text = jsonDecode(widget.patient)["last_name"] ?? "";
      _controllerDescription.text = jsonDecode(widget.patient)["description"] ?? "";
      _controllerMedList.text = jsonDecode(widget.patient)["med_list"] ?? "";
      _controllerLink.text = jsonDecode(widget.patient)["link"] ?? "";
      _controllerAge.text = jsonDecode(widget.patient)["age"].toString();
      _controllerImage.text = jsonDecode(widget.patient)["image"] ?? "";
      _controllerPhoneNumber.text = jsonDecode(widget.patient)["phone_number"] ?? "";
      _controllerDateOfBirth = jsonDecode(widget.patient)["date_of_birth"].toString();
      _controllerStreetAddress.text = jsonDecode(widget.patient)["street_address"] ?? "";
      _controllerCityAddress.text = jsonDecode(widget.patient)["city_address"]  ?? "";
      _controllerZipcodeAddress.text = jsonDecode(widget.patient)["zipcode_address"] ?? "";
      _controllerStateAddress.text = jsonDecode(widget.patient)["state_address"] ?? "";
      _controllerGender = jsonDecode(widget.patient)["gender"] ?? "Male";
      _controllerEmergencyContactMe.text = jsonDecode(widget.patient)["emergency_contact_name"] ?? "";
      _controllerEmergencyPhoneNumber.text = jsonDecode(widget.patient)["emergency_phone_number"] ?? "";
      _controllerRelationship = jsonDecode(widget.patient)["relationship"] ?? "Spouse";
      _controllerIsInHospital = "Yes";
      _controllerUser.text = jsonDecode(widget.patient)["user"] ?? "";
      for(var index = 0; index < jsonDecode(widget.patient)["tags"].length; index++){
        _controllerInitTags.add(jsonDecode(widget.patient)["tags"][index]["name"].toString());
      };
      for(var index = 0; index < jsonDecode(widget.patient)["treatment"].length; index++){
        _controllerInitTreatment.add(jsonDecode(widget.patient)["treatment"][index]["name"].toString());
      };
    super.initState();

  }

  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(
        leading: IconButton(
            icon: Icon(Icons.arrow_back),
            onPressed: (){
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => Patient(title: "Patients", type: widget.type),
                ),
              );
            }
        ),
        title: Text(widget.title),
      ),
      body: _isLoading ? Center(
          child : Column(
            mainAxisAlignment: MainAxisAlignment.center,//Center Column contents vertically,
            children: const [
              CircularProgressIndicator(),
              Text(
                'Loading . . .',
              ),
            ],
          )
      ) :  SingleChildScrollView(
        child: Stack(
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  _buildTextFieldFirstName(),
                  _buildTextFieldLastName(),
                  _buildTextFieldDescription(),
                  _buildTextFieldMedList(),
                  _buildTextFieldAge(),
                  _buildTextFieldLink(),
                  _buildTextFieldPhoneNumber(),
                  DateTimePicker(
                    initialValue: _controllerDateOfBirth,
                    firstDate: DateTime(2000),
                    lastDate: DateTime(2100),
                    dateLabelText: 'Date Of Birth',
                    onChanged: (val) => {_controllerDateOfBirth = val},
                    validator: (val) {},
                    onSaved: (val) {},
                  ),
                  _buildTextFieldStreetAddress(),
                  _buildTextFieldCityAddress(),
                  _buildTextFieldZipcodeAddress(),
                  _buildTextFieldStateAddress(),
                  _buildSelectFieldGender(),
                  _buildTextFieldEmergencyContactMe(),
                  _buildTextFieldEmergencyPhoneNumber(),
                  _buildSelectFieldRelationship(),
                  _buildSelectIsInHospital(),
                  _buildTextFieldUser(),
                  _buildTextFieldTags(),
                  _buildTextFieldTreatment(),
                  Padding(
                    padding: const EdgeInsets.only(top: 8.0),
                    child: FloatingActionButton.extended(
                      label: Text(
                        "save".toUpperCase(),
                        style: const TextStyle(
                          color: Colors.white,
                        ),
                      ),
                      onPressed: () {
                        setState(() => _isLoading = true);
                        List<String> imageLists = [];
                        List<dynamic> cTags = [];
                        for(var index=0; index < _controllerTags.getTags!.length; index++){
                          cTags.add({"name": _controllerTags.getTags![index]});
                        }
                        List<dynamic> cTreatment = [];
                        for(var index=0; index < _controllerTreatment.getTags!.length; index++){
                          cTreatment.add({"name": _controllerTags.getTags![index]});
                        }
                        PatientForm patientForm = PatientForm(
                          first_name: _controllerFirstName.text,
                          last_name: _controllerLastName.text,
                          description: _controllerDescription.text,
                          med_list: _controllerMedList.text,
                          age: _controllerAge.text,
                          link: _controllerLink.text,
                          phone_number: _controllerPhoneNumber.text,
                          date_of_birth: _controllerDateOfBirth,
                          street_address: _controllerStreetAddress.text,
                          city_address: _controllerCityAddress.text,
                          zipcode_address: _controllerZipcodeAddress.text,
                          state_address: _controllerStateAddress.text,
                          gender: _controllerGender,
                          emergency_contact_name: _controllerEmergencyContactMe.text,
                          emergency_phone_number: _controllerEmergencyPhoneNumber.text,
                          relationship: _controllerRelationship,
                          is_in_hospital: _controllerIsInHospital,
                          user: _controllerUser.text,
                          tags: cTags,
                          treatment: cTreatment,
                          image_lists: imageLists,
                        );
                        _apiService.updatePatient(jsonDecode(widget.patient)["id"], patientForm).then((response) {
                          setState(() => _isLoading = false);
                          if(response['status'] == "success"){
                            setState(() => _isLoading = false);
                            final snackBar = SnackBar(
                              content: const Text('Update Patient Successfully!'),
                            );
                            ScaffoldMessenger.of(context).showSnackBar(snackBar);
                          }
                          if(response["status"] == "error"){
                            final snackBar = SnackBar(
                              content: const Text('Some thing went wrong!'),
                            );
                            ScaffoldMessenger.of(context).showSnackBar(snackBar);
                          }
                        });
                      },
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTextFieldFirstName() {
    return TextField(
      controller: _controllerFirstName,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "First Name",
        errorText: _messageFirstName == ""? null : _messageFirstName,
      ),
      onChanged: (value) {
        bool isFieldValid = value.trim().isNotEmpty;
        if (!isFieldValid) {
          setState(() => _messageFirstName = "This Field is required.");
        }else{
          setState(() => _messageFirstName = "");
        }
      },
    );
  }

  Widget _buildTextFieldLastName() {
    return TextField(
      controller: _controllerLastName,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "Last Name",
        errorText: _messageLastName == ""? null : _messageLastName,
      ),
      onChanged: (value) {
        bool isFieldValid = value.trim().isNotEmpty;
        if (!isFieldValid) {
          setState(() => _messageLastName = "This Field is required.");
        }else{
          setState(() => _messageLastName = "");
        }
      },
    );
  }

  Widget _buildTextFieldDescription() {
    return TextField(
      controller: _controllerDescription,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "Description",
        errorText: _messageDescription == ""? null : _messageDescription,
      ),
    );
  }

  Widget _buildTextFieldMedList() {
    return TextField(
      controller: _controllerMedList,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "Med List",
        errorText: _messageMedList == ""? null : _messageMedList,
      ),
    );
  }

  Widget _buildTextFieldAge() {
    return TextField(
      controller: _controllerAge,
      keyboardType: const TextInputType.numberWithOptions(decimal: true),
      decoration: InputDecoration(
        labelText: "Age",
        errorText: _messageAge == ""? null : _messageAge,
      ),
      inputFormatters: <TextInputFormatter>[
        FilteringTextInputFormatter.digitsOnly
      ],
    );
  }

  Widget _buildTextFieldLink() {
    return TextField(
      controller: _controllerLink,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "Link",
        errorText: _messageLink == ""? null : _messageLink,
      ),
    );
  }

  Widget _buildTextFieldPhoneNumber() {
    return TextField(
      controller: _controllerPhoneNumber,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "Phone Number",
        errorText: _messagePhoneNumber == ""? null : _messagePhoneNumber,
      ),
    );
  }

  Widget _buildTextFieldStreetAddress() {
    return TextField(
      controller: _controllerStreetAddress,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "Street Address",
        errorText: _messageStreetAddress == ""? null : _messageStreetAddress,
      ),
    );
  }

  Widget _buildTextFieldCityAddress() {
    return TextField(
      controller: _controllerCityAddress,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "City Address",
        errorText: _messageCityAddress == ""? null : _messageCityAddress,
      ),
    );
  }

  Widget _buildTextFieldZipcodeAddress() {
    return TextField(
      controller: _controllerZipcodeAddress,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "Zipcode Address",
        errorText: _messageZipcodeAddress == ""? null : _messageZipcodeAddress,
      ),
    );
  }

  Widget _buildTextFieldStateAddress() {
    return TextField(
      controller: _controllerStateAddress,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "State Address",
        errorText: _messageStateAddress == ""? null : _messageStateAddress,
      ),
    );
  }

  Widget _buildSelectFieldGender() {
    return Row(
        children: [
          const Padding(
            padding: EdgeInsets.only(right: 10.0),
            child: Text(
              "Gender : ",
              style: TextStyle(fontSize: 17),
            ),
          ),
          DropdownButton<String>(
            value: _controllerGender,
            icon: const Icon(Icons.arrow_downward),
            elevation: 16,
            underline: Container(
              height: 2,
            ),
            onChanged: (String? value) {
            // This is called when the user selects an item.
              setState(() {
                _controllerGender = value!;
              });
            },
            items: _genderItems,
            )
        ]
    );
  }

  Widget _buildTextFieldEmergencyContactMe() {
    return TextField(
      controller: _controllerEmergencyContactMe,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "Emergency Contact Me",
        errorText: _messageEmergencyContactMe == ""? null : _messageEmergencyContactMe,
      ),
    );
  }

  Widget _buildTextFieldEmergencyPhoneNumber() {
    return TextField(
      controller: _controllerEmergencyPhoneNumber,
      keyboardType: TextInputType.text,
      decoration: InputDecoration(
        labelText: "Emergency Phone Number",
        errorText: _messageEmergencyPhoneNumber == ""? null : _messageEmergencyPhoneNumber,
      ),
    );
  }

  Widget _buildSelectFieldRelationship() {
    return Row(
      children: [
        const Padding(
          padding: EdgeInsets.only(right: 10.0),
          child: Text(
          "Relationship : ",
            style: TextStyle(fontSize: 17),
          ),
        ),
        DropdownButton<String>(
          value: _controllerRelationship,
          icon: const Icon(Icons.arrow_downward),
          elevation: 16,
          underline: Container(
            height: 2,
          ),
          onChanged: (String? value) {
            // This is called when the user selects an item.
            setState(() {
              _controllerRelationship = value!;
            });
          },
          items: _relationshipItems
        )
      ]
    );
  }

  Widget _buildSelectIsInHospital() {
    return Row(
        children: [
          const Padding(
            padding: EdgeInsets.only(right: 10.0),
            child: Text(
              "Is In Hospital : ",
              style: TextStyle(fontSize: 17),
            ),
          ),
          DropdownButton(
            value: _controllerIsInHospital,
            icon: const Icon(Icons.arrow_downward),
            elevation: 16,
            underline: Container(
              height: 2,
            ),
            onChanged: (String? value) {
            // This is called when the user selects an item.
              setState(() {
                _controllerIsInHospital = value!;
              });
            },
            items: _isInHospitalItems
          )
        ]
    );
  }

  Widget _buildTextFieldUser() {
    return TextField(
      controller: _controllerUser,
      keyboardType: TextInputType.number,
      decoration: InputDecoration(
        labelText: "User",
        errorText: _messageUser == ""? null : _messageUser,
      ),
      onChanged: (value) {
        bool isFieldValid = value.trim().isNotEmpty;
        if (!isFieldValid) {
          setState(() => _messageUser = "This Field is required.");
        }else{
          setState(() => _messageUser = "");
        }
      },
    );
  }

  Widget _buildTextFieldTags() {
    return TextFieldTags(
      textfieldTagsController: _controllerTags,
      initialTags: _controllerInitTags,
      textSeparators: const [','],
      letterCase: LetterCase.normal,
      validator: (String tag) {
        if (_controllerTags.getTags!.contains(tag)) {
          return 'you already entered that';
        }
        return null;
      },
      inputfieldBuilder:
          (context, tec, fn, error, onChanged, onSubmitted) {
        return ((context, sc, tags, onTagDelete) {
          return Padding(
            padding: const EdgeInsets.all(10.0),
            child: TextField(
              controller: tec,
              focusNode: fn,
              decoration: InputDecoration(
                isDense: true,
                border: const OutlineInputBorder(
                  borderSide: BorderSide(
                    color: Color.fromARGB(255, 74, 137, 92),
                    width: 3.0,
                  ),
                ),
                focusedBorder: const OutlineInputBorder(
                  borderSide: BorderSide(
                    color: Color.fromARGB(255, 74, 137, 92),
                    width: 3.0,
                  ),
                ),
                helperStyle: const TextStyle(
                  color: Color.fromARGB(255, 74, 137, 92),
                ),
                hintText: _controllerTags.hasTags ? '' : "Enter tag...",
                errorText: error,
                prefixIconConstraints:
                BoxConstraints(maxWidth: _distanceToField * 0.74),
                prefixIcon: tags.isNotEmpty
                    ? SingleChildScrollView(
                  controller: sc,
                  scrollDirection: Axis.horizontal,
                  child: Row(
                      children: tags.map((String tag) {
                        return Container(
                          decoration: const BoxDecoration(
                            borderRadius: BorderRadius.all(
                              Radius.circular(20.0),
                            ),
                            color: Color.fromARGB(255, 74, 137, 92),
                          ),
                          margin: const EdgeInsets.symmetric(
                              horizontal: 5.0),
                          padding: const EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 5.0),
                          child: Row(
                            mainAxisAlignment:
                            MainAxisAlignment.spaceBetween,
                            children: [
                              InkWell(
                                child: Text(
                                  '#$tag',
                                  style: const TextStyle(
                                      color: Colors.white),
                                ),
                                onTap: () {
                                  print("$tag selected");
                                },
                              ),
                              const SizedBox(width: 4.0),
                              InkWell(
                                child: const Icon(
                                  Icons.cancel,
                                  size: 14.0,
                                  color: Color.fromARGB(
                                      255, 233, 233, 233),
                                ),
                                onTap: () {
                                  onTagDelete(tag);
                                },
                              )
                            ],
                          ),
                        );
                      }).toList()),
                )
                    : null,
              ),
              onChanged: onChanged,
              onSubmitted: onSubmitted,
            ),
          );
        });
      },
    );
  }

  Widget _buildTextFieldTreatment() {
    return TextFieldTags(
      textfieldTagsController: _controllerTreatment,
      initialTags: _controllerInitTreatment,
      textSeparators: const [','],
      letterCase: LetterCase.normal,
      validator: (String tag) {
        if (_controllerTreatment.getTags!.contains(tag)) {
          return 'you already entered that';
        }
        return null;
      },
      inputfieldBuilder:
          (context, tec, fn, error, onChanged, onSubmitted) {
        return ((context, sc, tags, onTagDelete) {
          return Padding(
            padding: const EdgeInsets.all(10.0),
            child: TextField(
              controller: tec,
              focusNode: fn,
              decoration: InputDecoration(
                isDense: true,
                border: const OutlineInputBorder(
                  borderSide: BorderSide(
                    color: Color.fromARGB(255, 74, 137, 92),
                    width: 3.0,
                  ),
                ),
                focusedBorder: const OutlineInputBorder(
                  borderSide: BorderSide(
                    color: Color.fromARGB(255, 74, 137, 92),
                    width: 3.0,
                  ),
                ),
                helperStyle: const TextStyle(
                  color: Color.fromARGB(255, 74, 137, 92),
                ),
                hintText: _controllerTreatment.hasTags ? '' : "Enter treatment...",
                errorText: error,
                prefixIconConstraints:
                BoxConstraints(maxWidth: _distanceToField * 0.74),
                prefixIcon: tags.isNotEmpty
                    ? SingleChildScrollView(
                  controller: sc,
                  scrollDirection: Axis.horizontal,
                  child: Row(
                      children: tags.map((String tag) {
                        return Container(
                          decoration: const BoxDecoration(
                            borderRadius: BorderRadius.all(
                              Radius.circular(20.0),
                            ),
                            color: Color.fromARGB(255, 74, 137, 92),
                          ),
                          margin: const EdgeInsets.symmetric(
                              horizontal: 5.0),
                          padding: const EdgeInsets.symmetric(
                              horizontal: 10.0, vertical: 5.0),
                          child: Row(
                            mainAxisAlignment:
                            MainAxisAlignment.spaceBetween,
                            children: [
                              InkWell(
                                child: Text(
                                  '#$tag',
                                  style: const TextStyle(
                                      color: Colors.white),
                                ),
                                onTap: () {
                                  print("$tag selected");
                                },
                              ),
                              const SizedBox(width: 4.0),
                              InkWell(
                                child: const Icon(
                                  Icons.cancel,
                                  size: 14.0,
                                  color: Color.fromARGB(
                                      255, 233, 233, 233),
                                ),
                                onTap: () {
                                  onTagDelete(tag);
                                },
                              )
                            ],
                          ),
                        );
                      }).toList()),
                )
                    : null,
              ),
              onChanged: onChanged,
              onSubmitted: onSubmitted,
            ),
          );
        });
      },
    );
  }
}
