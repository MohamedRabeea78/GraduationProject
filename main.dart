import 'package:flutter/material.dart';
import 'package:toothy_match/screens/onboarding_page.dart';
import 'supabase_client.dart';
import 'screens/auth_check.dart';

Future<void> main() async {
  // Initialize Supabase
  await SupabaseClientManager.initialize();
  runApp(const ToothyMatchApp());
}

class ToothyMatchApp extends StatelessWidget {
  const ToothyMatchApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Toothy Match',
      theme: ThemeData(
        primarySwatch: Colors.teal,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home:  OnboardingPage(),
    );
  }
}
