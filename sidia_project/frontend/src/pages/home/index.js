/* eslint-disable no-unused-vars */
/* eslint-disable consistent-return */
/* eslint-disable prefer-destructuring */
/* eslint-disable prefer-template */
/* eslint-disable prefer-const */
/* eslint-disable guard-for-in */
/* eslint-disable no-restricted-syntax */
/* eslint-disable func-names */
/* eslint-disable camelcase */
/* eslint-disable react/destructuring-assignment */
/* eslint-disable react/jsx-indent */
/* eslint-disable class-methods-use-this */
import React from 'react'
import { message } from 'antd'
import { Helmet } from 'react-helmet'
import ChartCard from 'components/CleanUIComponents/ChartCard'
import config_server from "config.json"
// eslint-disable-next-line no-unused-vars
import C3Chart from 'react-c3js'


const colors = {
  primary: '#01a8fe',
  def: '#acb7bf',
  success: '#46be8a',
  danger: '#fb434a',
}

class DashboardAlpha extends React.Component {
  
  state = {
    title: null,
    actor: null,
    completed: null,
    data: [],
  }
  
  componentDidMount() {
    this.getCount('title')
    this.getCount('actor')
    this.getCount('completed')
    this.getTypeCount()
  }

  getCount = (param) => {

    let self = this
    let url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/stat/" + param + "/"

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
      
        if (param === 'title') {
          self.setState({ title: data_loaded.title_count })
        } else if (param === 'actor') {
          self.setState({ actor: data_loaded.actor_count })
        } else if (param === 'completed') {
          self.setState({ completed: data_loaded.completed })
        }

    }).catch(function (err) {
      
      console.log(err);

    });

  }
  

  getTypeCount = () => {

    let self = this
    let url = "http://" + config_server.ip + ":" + config_server.port + "/api/titles/stat/type/"

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

      // console.log(data_loaded.type_count)
      let data = data_loaded.type_count
      self.setState({ data })

    }).catch(function (err) {
      
      console.log(err);

    });

  }

  getRandomArbitrary(min, max) {
    let values  = []
    for (let i = 0; i <= 5; i+=1) {
      values.push(Math.round(Math.random() * (max - min) + min))
    }
    return values
  }

  prepareCard = (title_card, value) => {
      let v = this.getRandomArbitrary(10, 150)
      if ((title_card !== null) && (title_card !== undefined)) {  
        return (
                  <div className="col-xl-4">
                    <ChartCard
                      title={title_card}
                      amount={value}
                      chartProps={{
                        width: 120,
                        height: 107,
                        lines: [
                          {
                            values: v,
                            colors: {
                              area: 'rgba(199, 228, 255, 0.5)',
                              line: '#004585',
                            },
                          },
                        ],
                      }}
                    />
                  </div>)
      } 
                
                return (
                  <div className="col-xl-4">
                    <ChartCard
                      title="Loading.."
                      amount={0}
                      chartProps={{
                        width: 120,
                        height: 107,
                        lines: [
                          {
                            values: v,
                            colors: {
                              area: 'rgba(199, 228, 255, 0.5)',
                              line: '#004585',
                            },
                          },
                        ],
                      }}
                    />
                  </div>)
      
    
  }

  prepare_graph = () => {

    // const pie = {
    //   data: {
    //     columns: [['Primary', 30], ['Success', 120]],
    //     type: 'pie',
    //   },
    //   color: {
    //     pattern: [colors.primary, colors.success],
    //   },
    // }

    let data = [['Primary', 30], ['Success', 120]]

    // data.push(this.state.data.map((item) => {
    //     // return [item.title_type, (100 * item.qty / this.state.title).toFixed(2)]
    //     // return [item.title_type, 10]
    // }))
    console.log("<<< PIE >>>")
    console.log(data)
    const pie = {
      data: {
        columns: this.state.data.map((item) => { return [item.title_type, (100 * item.qty / this.state.title).toFixed(2)] }),
        type: 'pie',
      },
      // color: {
      //   pattern: [colors.primary, colors.success, colors.success, colors.success, colors.success, colors.success, colors.success, colors.success, colors.success, colors.success],
      // },
    }

    return (
      <div className="col-xl-4">
        <div className="mb-4">
          <C3Chart data={pie.data} color={pie.color} />
        </div>
      </div>)

  }

  render() {
    const {title, actor, completed} = this.state
    const items = this.state.data.map((item) => {
      // console.log(item.category)
        return this.prepareCard(item.title_type, item.qty + " ~ " + (100*item.qty/title).toFixed(2) + "%", title)
    })
    const pie_graph = () => this.prepare_graph()


    return (
      // <Authorize roles={['admin']} redirect to="/dashboard/beta">
      <div>
        <Helmet title="Dashboard" />
        <div className="utils__title utils__title--flat mb-3">
          <strong className="text-uppercase font-size-16">Statistics from Registered Titles</strong>
        </div>
        
        <div className="row">
            {this.prepareCard('Titles', title)}
            {this.prepareCard('Actors', actor)}
            {this.prepareCard('Completed Data', completed)}
        </div>
        <div className="row">
            {this.prepare_graph()}
            {/* {items} */}
        </div>
       
        {/* <div className="row">
          <div className="col-lg-12">
            <div className="card">
              <div className="card-header">
                <div className="utils__title">
                  <strong>Categories</strong>
                </div>
                <div className="utils__titleDescription">
                  Statistics from Titles by type
                </div>
              </div>
              <div className="card-body">
                <Table
                  className="utils__scrollTable"
                  scroll={{ x: '100%' }}
                  columns={tableColumns}
                  dataSource={tableData}
                  pagination={false}
                />
              </div>
            </div>
          </div>
        </div> */}
        {/* <div className="utils__title utils__title--flat mb-3">
          <strong className="text-uppercase font-size-16">Your Cards (3)</strong>
          <Button className="ml-3">View All</Button>
        </div> */}
        {/* <div className="row">
          <div className="col-lg-4">
            <PaymentCard
              icon="lnr lnr-bookmark"
              name="Matt Daemon"
              number="4512-XXXX-1678-7528"
              type="VISA"
              footer="Expires at 02/20"
              sum="$2,156.78"
            />
          </div>
          <div className="col-lg-4">
            <PaymentCard
              icon="lnr lnr-bookmark"
              name="David Beckham"
              number="8748-XXXX-1678-5416"
              type="MASTERCARD"
              footer="Expires at 03/22"
              sum="$560,245.35"
            />
          </div>
          <div className="col-lg-4">
            <PaymentCard
              icon="lnr lnr-hourglass"
              name="Mrs. Angelina Jolie"
              number="6546-XXXX-1678-1579"
              type="VISA"
              footer="Locked Temporary"
              sum="$1,467,98"
            />
          </div>
        </div>
        <div className="utils__title utils__title--flat mb-3">
          <strong className="text-uppercase font-size-16">Your Accounts (6)</strong>
          <Button className="ml-3">View All</Button>
        </div>
        <div className="row">
          <div className="col-lg-6">
            <PaymentAccount
              icon="lnr lnr-inbox"
              number="US 4658-1678-7528"
              footer="Current month charged: $10,200.00"
              sum="$2,156.78"
            />
          </div>
          <div className="col-lg-6">
            <PaymentAccount
              icon="lnr lnr-inbox"
              number="IBAN 445646-8748-4664-1678-5416"
              footer="Current month charged: $1,276.00"
              sum="$560,245.35"
            />
          </div>
        </div>
        <div className="row">
          <div className="col-lg-6">
            <PaymentAccount
              icon="lnr lnr-inbox"
              number="US 4658-1678-7528"
              footer="Current month charged: $10,200.00"
              sum="$2,156.78"
            />
          </div>
          <div className="col-lg-6">
            <PaymentAccount
              icon="lnr lnr-inbox"
              number="IBAN 445646-8748-4664-1678-5416"
              footer="Current month charged: $1,276.00"
              sum="$560,245.35"
            />
          </div>
        </div>
        <div className="utils__title mb-3">
          <strong className="text-uppercase font-size-16">Recent Transactions (167)</strong>
          <Button className="ml-3">View All</Button>
        </div>
        <div className="row">
          <div className="col-lg-12">
            <PaymentTransaction
              income={false}
              amount="-$100.00"
              info="US 4658-1678-7528"
              footer="To AMAZON COPR, NY, 1756"
            />
            <PaymentTransaction
              income
              amount="+27,080.00"
              info="4512-XXXX-1678-7528"
              footer="To DigitalOcean Cloud Hosting, Winnetka, LA"
            />
            <PaymentTransaction
              income={false}
              amount="-100,000.00"
              info="6245-XXXX-1678-3256"
              footer="To Tesla Cars, LA, USA"
            />
            <div className="text-center pb-5">
              <Button type="primary" className="width-200" loading>
                Load More...
              </Button>
            </div>
          </div>
        </div> */}
      {/* // </Authorize> */}
      </div>
    )
  }
}

export default DashboardAlpha
