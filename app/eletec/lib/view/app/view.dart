import 'package:eletec/I18n/i18n.dart';
import 'package:eletec/config/router.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:google_map_location_picker/generated/i18n.dart' as location_picker;

import 'bloc/app_bloc.dart';

class EletecApp extends StatefulWidget {
  
  @override
  State<EletecApp> createState() => EletecAppState();
}

class EletecAppState extends State<EletecApp> {

  @override
  Widget build(BuildContext context) => BlocProvider<AppBloc>(
    create: (context) => AppBloc(context)..add(AppInitial()),
    child: BlocBuilder<AppBloc, AppState>(
      builder: (context, state) {
        return MaterialApp( 
          title: 'Eletec',
          locale: state.locale,
          localizationsDelegates: const [
            location_picker.S.delegate,
            Localization.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
          ],
          supportedLocales: const <Locale>[
            Locale('en', ''),
            Locale('ar', ''),
          ],
          theme: ThemeData(
            primaryColor: Colors.blue,
            buttonTheme: ButtonThemeData(
              buttonColor: Colors.blue,
              hoverColor: Colors.green,
              shape: StadiumBorder(),
              textTheme: ButtonTextTheme.primary
            )
          ),
          onGenerateRoute: Router.instance.generator,
        );
      }
    )
  );
}
