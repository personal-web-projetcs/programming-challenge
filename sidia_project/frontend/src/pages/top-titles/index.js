/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable react/no-unused-state */
/* eslint-disable react/no-access-state-in-setstate */
/* eslint-disable react/destructuring-assignment */
/* eslint-disable guard-for-in */
/* eslint-disable no-restricted-syntax */
/* eslint-disable no-else-return */
/* eslint-disable no-unused-vars */
/* eslint-disable prefer-template */
/* eslint-disable dot-notation */
/* eslint-disable func-names */
/* eslint-disable prefer-const */
/* eslint-disable prefer-destructuring */
/* eslint-disable camelcase */
import React from 'react'
import { Table, Icon, Input, Button, message, Tag, Badge, DatePicker } from 'antd'
import { Helmet } from 'react-helmet'
import config_server from "config.json"
// import moment from 'moment'
// import Moment from 'react-moment'

// import table from './data.json'

// import styles from './style.module.scss'
const dateFormat = 'YYYY';

class TitleList extends React.Component {
  state = {
    tableData: [],
    avg: [],
    votes: [],
    data: [],
    filterDropdownVisible: false,
    searchText: '',
    filtered: false,
    loading: false,
    previous_page: null,
    next_page: null
  }
  
  componentDidMount() {
    this.getTopList("http://" + config_server.ip + ":" + config_server.port + "/api/titles/year/")
  }

  getTopList = (url) => {

    let self = this;

    self.setState({ loading: true });

    fetch(url, {
      method: 'GET',
    }).then(function (response) {
      if (response.status >= 400) {
        self.setState({loading: false})
        console.log(response)
        message.error('Bad response from server')
        throw new Error("Bad response from server")
      }
      return response.json();
    }).then(function (data_loaded) {

      console.log(data_loaded)
      self.setState({ data: data_loaded.results, tableData: data_loaded.results, previous_page: data_loaded.links.previous, next_page: data_loaded.links.next, loading: false })
      // console.log("<<<< LINK >>>>")
      // console.log(data_loaded.previous)
      // console.log(data_loaded.next)

    }).catch(function (err) {
      self.setState({ loading: false });
      console.log(err);
    });

  }

  getTopListByYear = (year) => {
    
    let self = this;

    let url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/year/" + year

    self.setState({ loading: true });

    fetch(url, {
      method: 'GET',
    }).then(function (response) {
      if (response.status >= 400) {
        self.setState({loading: false})
        console.log(response)
        message.error('Bad response from server')
        throw new Error("Bad response from server")
      }
      return response.json();
    }).then(function (data_loaded) {


      console.log(data_loaded)
      self.setState({ data: data_loaded.results, tableData: data_loaded.results, previous_page: data_loaded.links.previous, next_page: data_loaded.links.next, loading: false })
      // console.log("<<<< LINK >>>>")
      // console.log(data_loaded.previous)
      // console.log(data_loaded.next)

    }).catch(function (err) {
      self.setState({ loading: false });
      console.log(err);
    });

    
  }

  // handleChange = (pagination, filters, sorter) => {
  //   this.setState({
  //     filtered_type: filters
  //   });
    
  //   // this.getTopListByYear("type", filters, "http://" + config_server.ip + ":" + config_server.port + "/api/titles/types/filter/")
  // };

  handleClick = (id) => {
    let url

    if (id === "next")
      url = this.state.next_page
    else if (id === "previous")
      url = this.state.previous_page
    
    this.getTopList(url)
    // else
        // this.getTitleListFiltered("type", filters, url)
  }

  onInputChange = e => {
    this.setState({ searchText: e.target.value })
  }

  onSearch = () => {
    let year = this.state.searchText

    this.getTopListByYear(year)

  }

  linkSearchInput = node => {
    this.searchInput = node
  }

  render() {
    const { data, searchText, filtered, filterDropdownVisible, genre_list } = this.state

    const columns = [

      {
        title: 'ID',
        dataIndex: 'title_id',
        key: 'title_id',
        width: '8%',
        render: text => (
          <a className="utils__link--underlined" href="javascript: void(0);">
            {`#${text}`}
          </a>
        ),
        sorter: (a, b) => a.title_id - b.title_id,
      },
      {
        title: 'Title',
        dataIndex: 'original_title',
        // key: 'start_year',
        width: '25%',
        align: 'left',
        ellipsis: true,
        sorter: (a, b) => a.start_year - b.start_year,
        render: record => { return (record !== null) ? record : "-" }
      },
      {
        title: 'Rating',
        dataIndex: 'rating',
        key: 'average_rating',
        width: '10%',
        align: 'center',
        sorter: (a, b) => a.average_rating - b.average_rating,
        render: record => { return (record.average_rating !== null) ? record.average_rating : "-" }
      },
      {
        title: 'Votes',
        dataIndex: 'rating',
        key: 'num_votes',
        width: '10%',
        align: 'center',
        sorter: (a, b) => a.rating.num_votes - b.rating.num_votes,
        render: record => { return (record.num_votes !== null) ? record.num_votes : "-" }
      },
      {
        title: 'Start Year',
        dataIndex: 'start_year',
        align: 'center',
        width: '10%',
        sorter: (a, b) => a.start_year - b.start_year,
        render: text => (
      
          <a className="utils__link--underlined" href="javascript: void(0);">
            {text}
          </a>
    
        ),
        filterDropdown: (
          <div className="custom-filter-dropdown">
            <Input
              ref={this.linkSearchInput}
              placeholder="Filter Top Titles by year"
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
        title: 'End Year',
        dataIndex: 'end_year',
        // key: 'end_year',
        width: '8%',
        align: 'center',
        sorter: (a, b) => a.end_year - b.end_year,
        render: record => { return (record !== null) ? record : "-" }
      },
      {
        title: 'Runtime',
        dataIndex: 'runtime_minutes',
        // key: 'runtime_minutes',
        width: '8%',
        align: 'center',
        sorter: (a, b) => a.runtime_minutes - b.runtime_minutes,
        render: record => { return (record !== null) ? record + " min" : "-" }
      },
      {
        title: 'Adult ?',
        dataIndex: 'is_adult',
        // key: 'is_adult',
        width: '8%',
        align: 'center',
        render: (record) => { 
              
              if (record !== null) {
                if (record === true) {
                    return (
                      <Badge status="error" />
                    );
                } else {
                    return (
                      <Badge status="success" />
                    );
                }
              }
              return (
                <Badge status="warning" />
              ); 
            } ,
      },
      {
        title: 'Genres',
        dataIndex: 'genres',
        // key: 'genre',
        width: '20%',
        ellipsis: true,
        // sorter: (a, b) => a.genres.length - b.genres.length,
        render: record => { if (record === null) {
                              return (
                                <Tag color="orange">
                                  {"Undefined"}
                                </Tag>
                              )
                            } else {  
                              return record.map((genre, index) => {
                                return (
                                  <Tag color="geekblue">
                                    { record[index] }
                                  </Tag>
                                )
                              })
                            }
                          }  
          
      },
    ]

    return (
      <div>
        <Helmet title="Top Titles List" />
        <div className="card">
          <div className="card-header">
            <div className="utils__title">
              <strong>Top Rating List</strong>
            </div>
          </div>
          <div className="card-body">
            <Table
              rowKey="title_id"
              className="utils__scrollTable"
              scroll={{ x: '100%' }}
              columns={columns}
              dataSource={data}
              // onChange={this.handleChange}
              pagination={{ hideOnSinglePage:true }}
              loading={this.state.loading}
            />
            <br />
            <Button.Group>
              <Button type="ghost" onClick={() => this.handleClick("previous")} className="mr-1" disabled={this.state.previous_page === null}>
                <Icon type="left" />
                Previous
              </Button>
              <Button type="ghost" onClick={() => this.handleClick("next")} className="mr-1" disabled={this.state.next_page === null}>
                Next
                <Icon type="right" />
              </Button>
            </Button.Group>
          </div>
        </div>
      </div>
    )
  }
}

export default TitleList
