import argparse
import json

from flow_chart.flow_chart import FlowChart

if __name__ == '__main__':
    train_parser = argparse.ArgumentParser(description='Training arguments')

    # Add the arguments
    print('hey from train!!')
    train_parser.add_argument('--chart', type=json.loads, help='flow chart')
    args = train_parser.parse_args()
    flow_chart_json = args.chart

    print(flow_chart_json)
    print(type(flow_chart_json))

    flow_chart = FlowChart(flow_chart_json=flow_chart_json)
    flow_chart.run()
