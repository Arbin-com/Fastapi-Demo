export interface StartChannelRequest {
  test_name: string;
  channels: number[];
}

export interface AssignScheduleRequest {
  schedule_name: string;
  barcode?: string;
  capacity?: number;
  MVUD1?: number;
  MVUD2?: number;
  MVUD3?: number;
  MVUD4?: number;
  all_assign?: boolean;
  channel_index?: number;
}
