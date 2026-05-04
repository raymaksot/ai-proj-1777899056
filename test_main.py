import pytest
import sys
import main


def test_parse_csv_basic():
    data = main.parse_csv("a,1\nb,2")
    assert data == [('a', 1.0), ('b', 2.0)]


def test_parse_csv_negative():
    data = main.parse_csv("x,-5")
    assert data[0][1] == 0.0


def test_parse_csv_header_skip():
    data = main.parse_csv("name,value\nitem,10")
    assert data == [('item', 10.0)]


def test_parse_csv_missing_column():
    data = main.parse_csv("label\nlabel,20")
    assert data == [('label', 20.0)]


def test_parse_csv_empty():
    data = main.parse_csv("")
    assert data == []


def test_parse_csv_file_path_detection(capsys):
    with pytest.raises(SystemExit):
        main.parse_csv("data.csv")
    captured = capsys.readouterr()
    assert "Error: File reading is not supported" in captured.err


def test_draw_bar_chart_empty():
    chart = main.draw_bar_chart([])
    assert chart == "No data to display."


def test_draw_bar_chart_all_zero():
    data = [('A', 0), ('B', 0)]
    chart = main.draw_bar_chart(data)
    expected = "A |  (0.0)\nB |  (0.0)"
    assert chart == expected


def test_draw_bar_chart_normal():
    data = [('Apple', 10), ('Banana', 20)]
    chart = main.draw_bar_chart(data)
    lines = chart.split('\n')
    assert lines[0] == " Apple | ************************* (10.0)"
    assert lines[1] == "Banana | ************************************************** (20.0)"
    assert len(lines) == 2


def test_draw_bar_chart_custom_width():
    data = [('A', 50), ('B', 100)]
    chart = main.draw_bar_chart(data, max_width=10)
    lines = chart.split('\n')
    assert lines[0] == "A | ***** (50.0)"
    assert lines[1] == "B | ********** (100.0)"


def test_integration_sample_data(capsys):
    # Simulate running main without arguments (sample data)
    import main as m
    # Save and restore sys.argv
    old_argv = sys.argv
    sys.argv = ['main.py']
    try:
        m.main()
    finally:
        sys.argv = old_argv
    captured = capsys.readouterr()
    assert "Apples" in captured.out
    assert "Bananas" in captured.out
    assert "Figs" in captured.out