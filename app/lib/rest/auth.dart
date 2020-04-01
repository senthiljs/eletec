part of 'client.dart';

// ignore_for_file: non_constant_identifier_names

@JsonSerializable()
class OtpResponse extends Equatable {
  final String phone_number;

  OtpResponse(this.phone_number);

  @override
  List<Object> get props => [phone_number];

  static OtpResponse fromJson(Map<String, dynamic> json) =>
      _$PhoneGenerateFromJson(json);
  Map<String, dynamic> toJson() => _$PhoneGenerateToJson(this);
}