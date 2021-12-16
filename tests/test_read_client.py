from read_client import create_frame
import sqlalchemy


def test_create_frame(mocky_trade_socket_data):
    frame = create_frame(mocky_trade_socket_data)
    print(frame)


def test_frame_to_sql(mocky_trade_socket_data):
    pair = "PNTUSDT"
    engine = sqlalchemy.create_engine(f"sqlite:///:memory:")
    frame = create_frame(mocky_trade_socket_data)
    sql = frame.to_sql(pair, engine, if_exists="append", index=False)
    print(sql)
