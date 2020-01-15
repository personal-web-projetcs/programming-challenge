/* eslint-disable no-unused-vars */
/* eslint-disable prefer-template */
/* eslint-disable dot-notation */
/* eslint-disable func-names */
/* eslint-disable prefer-const */
/* eslint-disable prefer-destructuring */
/* eslint-disable camelcase */
import React from 'react'
import { Table, Icon, Input, Button, message } from 'antd'
import { Helmet } from 'react-helmet'
import axios from 'axios'
import config_server from "config.json"
// import table from './data.json'

// import styles from './style.module.scss'

class TitleList extends React.Component {
  state = {
    tableData: [],
    data: [],
    filterDropdownVisible: false,
    searchText: '',
    filtered: false,
    // nextPageURL: ''
  }

  componentDidMount() {
    this.get_title_list()
  }

  get_title_list = () => {

    let self = this;

    fetch("http://" + config_server.ip + ":" + config_server.port + "/api/titles/", {
      method: 'GET',
    }).then(function (response) {
      if (response.status >= 400) {
        message.error('Bad response from server');
        throw new Error("Bad response from server");
      }
      return response.json();
    }).then(function (data_loaded) {

      console.log(data_loaded.results)
      self.setState({ data: data_loaded.results, tableData: data_loaded.results })

    }).catch(function (err) {
      console.log(err);
    });

  }

  onInputChange = e => {
    this.setState({ searchText: e.target.value })
  }

  onSearch = () => {
    const { searchText, tableData } = this.state
    const reg = new RegExp(searchText, 'gi')
    this.setState({
      filterDropdownVisible: false,
      filtered: !!searchText,
      data: tableData
        .map(record => {
          const match = record.name.match(reg)
          if (!match) {
            return null
          }
          return {
            ...record,
            name: (
              <span>
                {record.name
                  .split(reg)
                  .map((text, i) =>
                    i > 0 ? [<span className="highlight">{match[0]}</span>, text] : text,
                  )}
              </span>
            ),
          }
        })
        .filter(record => !!record),
    })
  }

  linkSearchInput = node => {
    this.searchInput = node
  }

  render() {
    const { data, searchText, filtered, filterDropdownVisible } = this.state

    const columns = [

      {
        title: 'ID',
        dataIndex: 'title_id',
        key: 'title_id',
        render: text => (
          <a className="utils__link--underlined" href="javascript: void(0);">
            {`#${text}`}
          </a>
        ),
        sorter: (a, b) => a.id - b.id,
      },
      {
        title: 'Title',
        dataIndex: 'original_title',
        // key: 'original_title',
        sorter: (a, b) => a.name.length - b.name.length,
        render: text => (
          <a className="utils__link--underlined" href="javascript: void(0);">
            {text}
          </a>
        ),
        filterDropdown: (
          <div className="custom-filter-dropdown">
            <Input
              ref={this.linkSearchInput}
              placeholder="Search name"
              value={searchText}
              onChange={this.onInputChange}
              onPressEnter={this.onSearch}
            />
            <Button type="primary" onClick={this.onSearch}>
              Search
            </Button>
          </div>
        ),
        filterIcon: <Icon type="search" style={{ color: filtered ? '#108ee9' : '#aaa' }} />,
        filterDropdownVisible,
        onFilterDropdownVisibleChange: visible => {
          this.setState(
            {
              filterDropdownVisible: visible,
            },
            () => this.searchInput && this.searchInput.focus(),
          )
        },
      },
      {
        title: 'Type',
        dataIndex: 'title_type',
        // key: 'title_type',
        sorter: (a, b) => a.type.length - b.type.length,
      },
      {
        title: 'Adult ?',
        dataIndex: 'is_adult',
        // key: 'is_adult',
        sorter: (a, b) => a.status.length - b.status.length,
        render: record => <span className="font-size-12 badge badge-success">{record}</span>,
      },
      {
        title: 'Start Year',
        dataIndex: 'start_year',
        // key: 'start_year',
        sorter: (a, b) => a.attribute.length - b.attribute.length,
      },
      {
        title: 'End Year',
        dataIndex: 'end_year',
        // key: 'end_year',
        sorter: (a, b) => a.sku.length - b.sku.length,
      },
      {
        title: 'Runtime(Min)',
        dataIndex: 'runtime_minutes',
        // key: 'runtime_minutes',
        sorter: (a, b) => a.price - b.price,
      },
      {
        title: 'Genres',
        dataIndex: 'genre',
        // key: 'genre',
        sorter: (a, b) => a.quantity - b.quantity,
      },
      
      {
        title: 'Action',
        // key: 'action',
        render: () => (
          <span>
            <Button icon="edit" className="mr-1" size="small">
              View
            </Button>
            <Button icon="cross" size="small">
              Remove
            </Button>
          </span>
        ),
      },
    ]

    return (
      <div>
        <Helmet title="Title List" />
        <div className="card">
          <div className="card-header">
            <div className="utils__title">
              <strong>Title List</strong>
            </div>
          </div>
          <div className="card-body">
            <Table
              rowKey="title_id"
              className="utils__scrollTable"
              scroll={{ x: '100%' }}
              columns={columns}
              dataSource={data}
            />
          </div>
        </div>
      </div>
    )
  }
}

export default TitleList
