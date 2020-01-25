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

class TitleList extends React.Component {
  state = {
    page: 1,
    tableData: [],
    data: [],
    type_list: [],
    filtered_type: [],
    filterDropdownVisible: false,
    searchText: '',
    filtered: false,
    loading: false,
    previous_page: null,
    next_page: null
  }

  componentDidMount() {
    this.getTypeList("http://" + config_server.ip + ":" + config_server.port + "/api/titles/types/")
    this.getTitleList("http://" + config_server.ip + ":" + config_server.port + "/api/titles/")
  }

  getTypeList = (url) => {

    let self = this
    let type_list = []
    let i

    self.setState({ loading: true });
    fetch(url, {
      method: 'GET',
    }).then(function (response) {
      if (response.status >= 400) {
        self.setState({ loading: false });
        console.log(url)
        message.error('Bad response from server')
        throw new Error("Bad response from server")
      }
      return response.json();
    }).then(function (data_loaded) {

      
      for (i in data_loaded) {
        type_list.push({ "text": data_loaded[i].title_type, "value": data_loaded[i].title_type })
      }
      console.log("type list >>>>>>>>>>")
      console.log(type_list)
      self.setState({ type_list, loading: false })

    }).catch(function (err) {
      self.setState({ loading: false })
      console.log(err);
    });


  }

  getTitleList = (url) => {

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
      self.setState({ data: data_loaded.results, tableData: data_loaded.results, previous_page: data_loaded.previous, next_page: data_loaded.next, loading: false })

    }).catch(function (err) {
      self.setState({ loading: false });
      console.log(err);
    });

  }

  getTitleListFiltered = (filters, url) => {

    let self = this
    let item = {}
    let data_list = []
    let i
    let f
    
    
    this.setState({ loading: true });
    f = filters.title_type
    console.log(filters)
    for (i = 0; i < f.length; i+=1) {
      item["type-" + i] = f[i]
      data_list.push(item)
    }

    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_list[0])
      }).then(function (response) {
        if (response.status >= 400) {
          self.setState({ loading: false });
          message.error('Bad response from server');
          throw new Error("Bad response from server");
        }
        return response.json();
      }).then(function (data_loaded) {
          console.log("filtered")
          console.log(data_loaded)
          if ((data_loaded !== null) && (data_loaded !== undefined)) {
          //   // console.log("Consulta de Insumos realizada com sucesso");
          //   // console.log(data_loaded);

            self.setState({ data: data_loaded.results, tableData: data_loaded.results, previous_page: data_loaded.previous, next_page: data_loaded.next, loading: false })
            
          //   // self.setState({ tableData: dados.data });
          //   // self.setState({ data: dados.data });
          }

      }).catch(function (err) {
        self.setState({ loading: false });
        console.log(err)
      });

  }

  onHandleTable = (pagination, filters) => {
    let url = ""
    let filter_last = this.state.filtered_type.sort()
    let filter_current = filters.title_type.sort()

    if ((filter_current.length === 0) && (filter_last.length > 0)) {
      console.log("Zerou filtro")
      this.setState({ filtered_type: [] })
      url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/"
      this.getTitleList(url)
    } else if (JSON.stringify(filter_last) !== JSON.stringify(filter_current)) {
      console.log("Mudou o filtro")
      this.setState({ filtered_type: filter_current })
      url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/types/filter/"
      this.getTitleListFiltered({title_type: filter_current}, url)
    }

  }

  handleClick = (id) => {
    let filters = this.state.filtered_type
    let url
    let page = this.state.page

    if (id === "next") {
      url = this.state.next_page
      this.setState({ page: page + 1 })
    } else if (id === "previous") {
      url = this.state.previous_page
      this.setState({ page: page - 1 })
    }

    if (filters.length === 0) {
        this.getTitleList(url)
    } else {
      console.log(filters)
      this.getTitleListFiltered({title_type: filters}, url)
    }

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
          const match = record.original_title.match(reg)
          if (!match) {
            return null
          }
          return {
            ...record,
            original_title: (
              <span>
                {record.original_title
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
    const { data, searchText, filtered, filterDropdownVisible, type_list } = this.state

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
        // key: 'original_title',
        width: '20%',
        ellipsis: true,
        sorter: (a, b) => a.original_title.length - b.original_title.length,
        render: text => (
      
          <a className="utils__link--underlined" href="javascript: void(0);">
            {text}
          </a>
    
        ),
        filterDropdown: (
          <div className="custom-filter-dropdown">
            <Input
              ref={this.linkSearchInput}
              placeholder="Search title"
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
        width: '10%',
        align: 'center',
        render: record => { return (record !== null) ? record : "-" },
        filters: type_list,
        onFilter: (value, record) => record.title_type.includes(value)
      },
      {
        title: 'Adult ?',
        dataIndex: 'is_adult',
        // key: 'is_adult',
        width: '5%',
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
        title: 'Start Year',
        dataIndex: 'start_year',
        // key: 'start_year',
        width: '8%',
        align: 'center',
        sorter: (a, b) => a.start_year - b.start_year,
        render: record => { return (record !== null) ? record : "-" }
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
        title: 'Rating',
        dataIndex: 'rating',
        key: 'average_rating',
        width: '8%',
        align: 'center',
        sorter: (a, b) => a.average_rating - b.average_rating,
        render: record => { return (record) ? record.average_rating : "-" }
      },
      {
        title: 'Genres',
        dataIndex: 'genres',
        // key: 'genre',
        width: '20%',
        sorter: (a, b) => a.genres.length - b.genres.length,
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
      
      // {
      //   title: 'Action',
      //   // key: 'action',
      //   render: () => (
      //     <span>
      //       <Button icon="edit" className="mr-1" size="small">
      //         View
      //       </Button>
      //       {/* <Button icon="cross" size="small">
      //         Remove
      //       </Button> */}
      //     </span>
      //   ),
      // },
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
              onChange={this.onHandleTable}
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
