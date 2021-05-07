import 'package:area_mobile/account/account.dart';
import 'package:area_mobile/auth/login.dart';
import 'package:area_mobile/auth/reset.dart';
import 'package:area_mobile/home.dart';
import 'package:area_mobile/services/createServicePage.dart';
import 'package:area_mobile/services/servicePage.dart';
import 'package:area_mobile/auth/register.dart';
import 'package:area_mobile/settings/settings.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

/// The main class who handle the route.
class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.grey,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      routes: {
        LoginPage.routeName: (context) => LoginPage(),
        RegisterPage.routeName: (context) => RegisterPage(),
        AccountPage.routeName: (context) => AccountPage(),
        ServicePage.routeName: (context) => ServicePage(),
        CreateServicePage.routeName: (context) => CreateServicePage(),
        HomePage.routeName: (context) => HomePage(userName: "UserName"),
        SettingsPage.routeName: (context) => SettingsPage(),
        ResetPage.routeName: (context) => ResetPage()
      },
    );
  }
}
