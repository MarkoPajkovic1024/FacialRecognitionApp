import 'dart:convert';
import 'dart:io';

import 'package:doctor/api/api.dart';
import 'package:doctor/components/profile_item.dart';
import 'package:flutter/material.dart';
import 'package:gallery_saver/gallery_saver.dart';
import 'package:image_picker/image_picker.dart';
import 'package:path_provider/path_provider.dart';
//import 'package:image/image.dart';

class ViewPatient extends StatefulWidget {
  const ViewPatient({Key? key, required this.title, required this.patient, required this.type}) : super(key: key);

  final String title;
  final dynamic patient;
  final String type;

  @override
  State<ViewPatient> createState() => _ViewPatientState();
}

class _ViewPatientState extends State<ViewPatient> {
  bool _isLoading = false;
  String url  = "";
  late String description = "";
  ApiService _apiService = ApiService();

  bool multiFlag = false;
  List<XFile>? imageFileList = [];
  final ImagePicker imgpicker = ImagePicker();

  chooseCamera() async {
    final choosedimage = await imgpicker.pickImage(source: ImageSource.camera);
    dynamic result = "";
    dynamic dir = "";
    if(choosedimage != null){
      GallerySaver.saveImage(choosedimage.path);
      SnackBar snackBar;
      setState(() {
        _isLoading = true;
      });
      _apiService.uploadImageFileVerify(choosedimage, jsonDecode(widget.patient)["id"]).then((response) =>{
        setState(() {
          _isLoading = false;
        }),
        dir = Directory(choosedimage.path),
        dir.deleteSync(recursive: true),
        result = jsonDecode(response),
        if(result["status"]){
            snackBar = const SnackBar(
              content: Text('Face Verify Successfully!'),
            ),
            ScaffoldMessenger.of(context).showSnackBar(snackBar),
          }else{
          snackBar = const SnackBar(
            content: Text('Face Verify Failed!'),
          ),
          ScaffoldMessenger.of(context).showSnackBar(snackBar),
        }
      });
      }
    }

  void chooseImages() async {
    final choosedimages = await imgpicker.pickMultiImage();
    if (choosedimages != null) {
      imageFileList = choosedimages;
      setState((){
        multiFlag = true;
      });
    }
  }

  void uploadImages() async {
    setState(() {
      _isLoading = true;
    });
    SnackBar snackBar;
    await _apiService.uploadImageFiles(imageFileList, jsonDecode(widget.patient)["id"]).then((response) => {
      setState(() {
        multiFlag = false;
        _isLoading = false;
      }),
      snackBar = const SnackBar(
        content: Text('Uploading files successfully!'),
       ),
      ScaffoldMessenger.of(context).showSnackBar(snackBar),
      setState(() {
      }),
    });
  }


  @override
  void initState() {
    // _apiService.getPatientImage(jsonDecode(widget.patient)["id"]).then((response) => {
    //    url = "http://10.10.11.226:8000" + jsonDecode(response!)["image_lists"][0]["image"],
    //   setState(() {
    //
    //   }),
    // });
    print(jsonDecode(widget.patient)["id"]);
    super.initState();
  }
  @override
  Widget build(BuildContext context) {

    String changeString(value){
        var ss = "";
        if(value.length != 0){
          for(var i = 0; i < value.length ; i++){
            ss = ss + value[i]["name"] + ",";
            ss = ss.substring(0, ss.length - 1);
          }
        }else{
          ss = "N/A";
        }
        return ss;
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body:Scrollbar(
        child: _isLoading ? Center(
            child : Column(
              mainAxisAlignment: MainAxisAlignment.center,//Center Column contents vertically,
              children: const [
                CircularProgressIndicator(),
                Text(
                  'Loading . . .',
                ),
              ],
            )
        ) : ListView(
          children: <Widget>[
              Container(
                width: 10,
                height: 20,
                alignment: Alignment.topCenter,
              ),
              SizedBox(
                  width: double.infinity,
                  child: CircleAvatar(
                      minRadius: 45,
                      backgroundColor: Colors.blueAccent,
                      foregroundColor: const Color(0xffffffff),
                      child: Text(
                        jsonDecode(widget.patient)["first_name"].substring(0, 1).toUpperCase() +
                            jsonDecode(widget.patient)["last_name"].substring(0, 1).toUpperCase(),
                        style: TextStyle(fontSize: 40),
                      )
                    ),
                  ),
              const SizedBox(
                width: 10,
                height: 20,
              ),
            widget.type == "only" ? Padding(
                  padding: const EdgeInsets.all(6.0),
                  child: Row(
                      mainAxisAlignment: MainAxisAlignment.center, //Center Row contents horizontally,
                      //crossAxisAlignment: CrossAxisAlignment.center,//Center Row contents vertically,
                      children: [FloatingActionButton.extended(
                        onPressed: () {
                          chooseCamera();
                        },
                        label: const Text(
                            "Take a picture"
                        ),
                      ),]
                  )
              ) : Container(),
              Padding(
                padding: const EdgeInsets.only(left: 10.0, right:10.0),
                child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: <Widget>[
                  ProfileItem(
                    title: "First Name",
                    icon: Icons.account_box_outlined,
                    value: jsonDecode(widget.patient)["first_name"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Last Name",
                      icon: Icons.account_box_outlined,
                      value: jsonDecode(widget.patient)["last_name"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Age",
                      icon: Icons.data_usage_outlined,
                      value: jsonDecode(widget.patient)["age"].toString()
                  ),
                  ProfileItem(
                      title: "Med List",
                      icon: Icons.auto_fix_high,
                      value: jsonDecode(widget.patient)["med_list"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Phone Number",
                      icon: Icons.phone,
                      value: jsonDecode(widget.patient)["phone_number"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Date of Birth",
                      icon: Icons.date_range,
                      value: jsonDecode(widget.patient)["date_of_birth"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Street Address",
                      icon: Icons.terrain,
                      value: jsonDecode(widget.patient)["street_address"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "City Address",
                      icon: Icons.terrain,
                      value: jsonDecode(widget.patient)["city_address"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Zipcode Address",
                      icon: Icons.terrain,
                      value: jsonDecode(widget.patient)["zipcode_address"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "State Address",
                      icon: Icons.terrain,
                      value: jsonDecode(widget.patient)["state_address"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Link",
                      icon: Icons.link,
                      value: jsonDecode(widget.patient)["link"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Emergency Contact Name",
                      icon: Icons.account_box_outlined,
                      value: jsonDecode(widget.patient)["emergency_contact_name"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Emergency Phone Number",
                      icon: Icons.phone,
                      value: jsonDecode(widget.patient)["emergency_phone_number"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Relationship",
                      icon: Icons.link,
                      value: jsonDecode(widget.patient)["relationship"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Gender",
                      icon: Icons.transgender,
                      value: jsonDecode(widget.patient)["Gender"] ?? "N/A"
                  ),
                  ProfileItem(
                      title: "Is In Hospital",
                      icon: Icons.local_hospital,
                      value: jsonDecode(widget.patient)["Is In Hospital"] ?? "N/A"
                  ),
                  widget.type == "only" ? ProfileItem(
                      title: "Tags",
                      icon: Icons.apps_outlined,
                      value: changeString(jsonDecode(widget.patient)["tags"])
                  ) : Container(),
                  widget.type == "only" ? ProfileItem(
                      title: "Treatment",
                      icon: Icons.apps_outlined,
                      value: changeString(jsonDecode(widget.patient)["treatment"])
                  ) : Container(),
                  ]
                ),
              ),
            multiFlag ? Padding(
              padding: const EdgeInsets.all(16.0),
              child: Wrap(
                  children: imageFileList!.map((imageone){
                    return Container(
                        child:Card(
                          child: Container(
                            height: 150, width:150,
                            child: Image.file(File(imageone.path)),
                          ),
                        )
                    );
                  }).toList()
              ),
            ): const Padding(
              padding: EdgeInsets.all(0.0),
            ),
            widget.type == "only" ? Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                    mainAxisAlignment: MainAxisAlignment.center, //Center Row contents horizontally,
                    //crossAxisAlignment: CrossAxisAlignment.center,//Center Row contents vertically,
                    children: [
                      FloatingActionButton.extended(
                        onPressed: () {
                          chooseImages();
                        },
                        label: Text(
                            multiFlag ? "Change Image files" : "Open Image files"
                        ),
                      ),
                      multiFlag ? FloatingActionButton.extended(
                        onPressed: () {
                          uploadImages();
                        },
                        label: const Text(
                            "Upload Image files"
                        ),
                      ) : Container()
                    ]
                )
            ) : Container(),
          ],
        )
      ),
    );
  }

}


