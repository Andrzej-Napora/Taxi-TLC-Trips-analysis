from download_parquet_file import BASE_URL, download_parquet_file


def test_download(requests_mock,tmp_path):

    date_str = "2026-01"
    taxi_type = "yellow"
    filename = f"{taxi_type}_tripdata_{date_str}.parquet"
    expected_url = f"{BASE_URL}/{filename}"
    test_content = b"test parquet content"

    requests_mock.get(expected_url,content=test_content,status_code = 200)

    result = download_parquet_file(date_str,taxi_type,tmp_path,set())

    download_file = tmp_path/filename

    assert result is True
    assert download_file.exists()
    assert download_file.read_bytes() == test_content
    assert requests_mock.call_count == 1

def test_donwload_skip(requests_mock,tmp_path):

    date_str = "2026-01"
    taxi_type = "yellow"
    filename = f"{taxi_type}_tripdata_{date_str}.parquet"
    expected_url = f"{BASE_URL}/{filename}"

    requests_mock.get(expected_url,text="requests_mock done")

    taxi_set = {filename}

    result = download_parquet_file(date_str,taxi_type,tmp_path,taxi_set)

    assert result is False
    assert requests_mock.call_count == 0