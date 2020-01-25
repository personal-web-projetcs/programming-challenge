/* eslint-disable object-shorthand */
/* eslint-disable no-unused-vars */
/* eslint-disable consistent-return */
/* eslint-disable array-callback-return */
/* eslint-disable no-unused-expressions */
/* eslint-disable import/no-extraneous-dependencies */
/* eslint-disable react/no-unused-state */
/* eslint-disable react/no-access-state-in-setstate */
/* eslint-disable react/destructuring-assignment */
/* eslint-disable guard-for-in */
/* eslint-disable no-restricted-syntax */
/* eslint-disable no-else-return */
/* eslint-disable prefer-template */
/* eslint-disable dot-notation */
/* eslint-disable func-names */
/* eslint-disable prefer-const */
/* eslint-disable prefer-destructuring */
/* eslint-disable camelcase */
import React from 'react'
import { Table, Icon, Input, Button, message, Tag, Badge } from 'antd'
import { Helmet } from 'react-helmet'
import config_server from "config.json"
// import moment from 'moment'
// import Moment from 'react-moment'

// import table from './data.json'

// import styles from './style.module.scss'

class TitleList extends React.Component {
  state = {
    pagination: {}, 
    tableData: [],
    avg: [],
    votes: [],
    data: [],

    filterDropdownVisible: false,
    searchText: '',
    filtered: false,
    
    loading: false,
    previous_page: null,
    next_page: null,

    genre_list: [],
    genre_filter_list: [],
    is_genre_filtered: false
  }
  
  componentDidMount() {
    this.getGenreList()
    this.getTopList(1)
  }

  getTopList = (page) => {

    let self = this;
    let url = ""

    let search_by_year = this.state.searchText
    if (search_by_year !== '') {
      url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/top/" + search_by_year + "/?page=" + page
    } else {
      url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/top/?page=" + page
    }
    
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

      // let pagination = {current: page, next: data_loaded.links.next, previous: data_loaded.links.previous, total: data_loaded.count}

      let pagination = self.state.pagination
      
      pagination = {current: page, total: data_loaded.count}

      console.log("Sucess GET >>>>>")
      console.log(data_loaded.results)
      
      self.setState({ data: data_loaded.results, tableData: data_loaded.results, loading: false, pagination })

    }).catch(function (err) {
      self.setState({ loading: false });
      console.log(err);
    });

  }


  getTopListFiltered = (page, filters) => {

    let self = this
    let genres = {}
    let fg = []
    let url = ""
    let search_by_year = this.state.searchText

    this.setState({ loading: true })

    if (search_by_year !== '') {
      url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/top/" + search_by_year + "/?page=" + page
      console.log("teste ano - " + url)
    } else {
      url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/top/?page=" + page
      console.log("teste sem ano - " + url)
    }

    genres = {"genres": { "data": filters  }}
    console.log(genres)

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(genres)
      }).then(function (response) {
        if (response.status >= 400) {
          self.setState({ loading: false })
          message.error('Bad response from server')
          throw new Error("Bad response from server")
        }
        return response.json();
      }).then(function (data_loaded) {
      
        // let pagination = {current: page, next: data_loaded.links.next, previous: data_loaded.links.previous, total: data_loaded.count}

        let pagination = self.state.pagination
        
        pagination = {current: page, total: data_loaded.count}

        // for (let i in data) {
        //   if (data[i].genres === null) {
        //     data[i].genres = ["Undefined"]
        //   }
        // }

        console.log("Sucess POST >>>>>")
        console.log(data_loaded.results)
        
        self.setState({ data: data_loaded.results, tableData: data_loaded.results, loading: false, pagination, is_genre_filtered: true })

      }).catch(function (err) {
        console.log("ERROR >>>>>")
        self.setState({ loading: false })
        console.log(err)
      });

  }


  // getTopListByYear = (year) => {
    
  //   let self = this;

  //   let url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/top/" + year

  //   self.setState({ loading: true });

  //   fetch(url, {
  //     method: 'GET',
  //   }).then(function (response) {
  //     if (response.status >= 400) {
  //       self.setState({loading: false})
  //       console.log(response)
  //       message.error('Bad response from server')
  //       throw new Error("Bad response from server")
  //     }
  //     return response.json();
  //   }).then(function (data_loaded) {


  //     console.log(data_loaded)
  //     self.setState({ data: data_loaded.results, tableData: data_loaded.results, previous_page: data_loaded.links.previous, next_page: data_loaded.links.next, loading: false })
  //     // console.log("<<<< LINK >>>>")
  //     // console.log(data_loaded.previous)
  //     // console.log(data_loaded.next)

  //   }).catch(function (err) {
  //     self.setState({ loading: false });
  //     console.log(err);
  //   });

    
  // }

  getGenreList = () => {

    let self = this
    const url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/genres/"
    let i
    let genres = []

    fetch(url, {
      method: 'GET',
    }).then(function (response) {
      if (response.status >= 400) {
        console.log(url)
        message.error('Bad response from server')
        throw new Error("Bad response from server")
      }
      return response.json();
    }).then(function (data_loaded) {

      for (i in data_loaded) {
        console.log(data_loaded[i])
        genres.push({ "text": data_loaded[i].genre, "value": data_loaded[i].genre })
      }

      self.setState({ genre_list: genres })

    }).catch(function (err) {
      
      console.log(err);
    });


  }

  // onHandleTable = (pagination, filters, sorter)
  onHandleTable = (pagination, filters) => {
    let filter_last = this.state.genre_filter_list.sort()
    let filter_current = []
    
    if ((filters.genres !== null) && (filters.genres !== undefined)) {
      filter_current = filters.genres.sort()
    }

    if ((filter_current.length === 0) && (filter_last.length > 0)) {
      console.log("Zerou filtro")
      this.setState({ genre_filter_list: [], is_genre_filtered: false })
      this.getTopList(1)
    } else if (JSON.stringify(filter_last) !== JSON.stringify(filter_current)) {
      console.log("Mudou o filtro")
      this.setState({ genre_filter_list: filter_current })
      this.getTopListFiltered(1, filter_current)
    } else if ((filter_current.length === 0) && (filter_last.length === 0)) {
      console.log("Mudou de Página sem filtro")
      this.getTopList(pagination.current)
    } else if (JSON.stringify(filter_last) === JSON.stringify(filter_current)) {
      console.log("Mudou de Página com filtro")
      this.getTopListFiltered(pagination.current, filter_current)
    }
    
  }

  onInputChange = e => {
    if ((/^\d+$/.test(e.target.value)) || (e.target.value === ""))
      this.setState({ searchText: e.target.value })
  }

  onSearch = () => {
    const is_genre_filtered = this.state.is_genre_filtered

    if (is_genre_filtered) {
      let filters = this.state.genre_filter_list
      console.log("Filtered")
      this.getTopListFiltered(1, filters)
    } else {
      console.log("No Filter")
      this.getTopList(1)
    }

  }

  linkSearchInput = node => {
    this.searchInput = node
  }

  render() {
    const { data, searchText, filtered, filterDropdownVisible, pagination, genre_list, loading, is_genre_filtered, genre_filter_list } = this.state

    const columns = [

      {
        title: 'ID',
        dataIndex: 'title_id',
        key: 'title_id',
        width: '8%',
        render: text => (
          <a className="utils__link--underlined" href="">
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
      
          <a className="utils__link--underlined" href="">
            {text}
          </a>
    
        ),
        filterDropdown: (
          <div className="custom-filter-dropdown">
            <Input
              ref={this.linkSearchInput}
              placeholder="Filter Top Titles by Year"
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

        render: (record) => { return record.map((genre) => {
                                  if (genre !== "Undefined") {
                                    return (
                                      <Tag color="geekblue">
                                        { genre }
                                      </Tag>
                                    )
                                  } else {
                                    return (
                                      <Tag color="orange">
                                        { "Undefined" }
                                      </Tag>
                                    )
                                  }

                                  })
      },
      filters: genre_list,
        
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
              onChange={this.onHandleTable}
              pagination={{ current: pagination.current, total: pagination.total }}
              loading={loading}
            />
          </div>
        </div>
      </div>
    )
  }
}

export default TitleList
