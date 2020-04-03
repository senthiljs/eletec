import 'dart:async';

import 'package:equatable/equatable.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:rxdart/rxdart.dart';

import 'package:eletec/plugs/flutter_form_builder/flutter_form_builder.dart';
import 'package:eletec/rest/client.dart';
import 'package:eletec/view/loading/bloc/loading_bloc.dart';
import 'package:eletec/view/app/app.dart';

import 'package:bloc/bloc.dart';

part 'login_event.dart';
part 'login_state.dart';

class LoginBloc extends Bloc<LoginEvent, LoginState> {
  final GlobalKey<FormBuilderState> formKey = GlobalKey<FormBuilderState>();

  final BuildContext context;

  LoginBloc(this.context);

  @override
  LoginState get initialState => LoginState.initial();

  @override
  Stream<LoginState> mapEventToState(
    LoginEvent event,
  ) async* {
    if (event is GetOTP) {
      BlocProvider.of<AppBloc>(context).add(ShowLoading());
      
      // if (formKey.currentState.saveAndValidate()) {
      //   yield state.copyWith(loading: true);

      //   FocusScope.of(context).requestFocus(FocusNode());
      //   BlocProvider.of<LoadingBloc>(context).add(ShowDialog());

      //   RestService.instance.phoneGenerate(formKey.currentState.value).then((res) {
      //     add(ResponseOTP(res));
      //   }).catchError((error) {
      //     formKey.currentState.setErrors(error?.response?.data);
      //   }).whenComplete(() {
      //     BlocProvider.of<LoadingBloc>(context).add(DismissDialog());
      //   });
      // }

      // OverlayEntry overlayEntry = OverlayEntry(
      //   builder: (_) =>   
        // GestureDetector(
        //   behavior: HitTestBehavior.translucent,
        //   onTap: () {
        //   },
        //   child: Container(
        //     color: Colors.black45, 
        //     height: 100,
        //     width: 100,
        //     child: CupertinoActivityIndicator(radius: 12)
        //   )
        // )
      // Positioned(
      //   top: MediaQuery.of(context).size.height * 0.5,
      //   child: Material(
      //     color: Colors.transparent,
      //     child: Center(
      //       child: Container(
      //         child: Padding(
      //           padding: EdgeInsets.all(20),
      //           child: CupertinoActivityIndicator(radius: 12), 
      //         ),
      //         color: Colors.black26
      //       )
      //     )
      //   ))
      // );

      // Overlay.of(context).insert(overlayEntry);
      // new Future.delayed(Duration(seconds: 2)).then((value) {
      //   overlayEntry.remove();
      // });
    }

    if (event is ResponseOTP) {
      yield state.copyWith(
        step: 1, 
        loading: false,
        otp: event.result
      );

      Scaffold.of(context)..hideCurrentSnackBar()..showSnackBar(
        SnackBar(
          content: Text('SMS sent successfully')
        ),
      );

      RangeStream(60, 0)
        .interval(Duration(seconds: 1))
        .listen((i) => add(Timer(i)));
    }

    if (event is Timer) {
      yield state.copyWith(timer: event.timer);
    }

    if (event is ResendOTP) {
      yield state.copyWith(
        step: 0,
        timer: 60,
      );
    }

    if (event is FormSubmitted) {
      if (formKey.currentState.saveAndValidate()) {
        yield state.copyWith(loading: true);
        
        FocusScope.of(context).requestFocus(FocusNode());
        BlocProvider.of<LoadingBloc>(context).add(ShowDialog());
        RestService.instance.phoneValidate(formKey.currentState.value).then((res) {
          BlocProvider.of<AppBloc>(context).add(SignedIn(res.token));
        }).catchError((error) {
          formKey.currentState.setErrors(error?.response?.data);
        }).whenComplete(() {
          BlocProvider.of<LoadingBloc>(context).add(DismissDialog());
        });
      }
    }
  }

  @override
  Future<void> close() {
    return super.close();
  }
}
