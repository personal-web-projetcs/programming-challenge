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
/* eslint-disable react/no-unused-state */
/* eslint-disable no-unused-vars */
import React from 'react'
import { Button, Table, message } from 'antd'
import { Helmet } from 'react-helmet'
import PaymentCard from 'components/CleanUIComponents/PaymentCard'
import PaymentAccount from 'components/CleanUIComponents/PaymentAccount'
import PaymentTransaction from 'components/CleanUIComponents/PaymentTransaction'
import ChartCard from 'components/CleanUIComponents/ChartCard'
import Authorize from 'components/LayoutComponents/Authorize'
import config_server from "config.json"


class DashboardAlpha extends React.Component {
  state = {
    title_count: 0,
    actor_count: 0,
    data: []
  }
  
  componentDidMount() {
    this.getCount('title')
    this.getCount('actor')
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

      if (param === 'title')
        self.setState({ title_count: data_loaded.title_count })
      else if (param === 'actor')
        self.setState({ actor_count: data_loaded.actor_count })

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

  render() {
    
    const items = this.state.data.map((item) => {
      // console.log(item.category)
      return  (<div className="col-xl-4">
                  <ChartCard
                    title={item.title_type}
                    amount={item.qty}
                    chartProps={{
                      width: 120,
                      height: 107,
                      lines: [
                        {
                          values: [2, 11, 8, 14, 18, 20, 26],
                          colors: {
                            area: 'rgba(199, 228, 255, 0.5)',
                            line: '#004585',
                          },
                        },
                      ],
                    }}
                  />
               </div>)

    })
    const {title_count, actor_count} = this.state

    return (
      <Authorize roles={['admin']} redirect to="/dashboard/beta">
        <Helmet title="Dashboard" />
        <div className="utils__title utils__title--flat mb-3">
          <strong className="text-uppercase font-size-16">Statistics from Registered Titles</strong>
        </div>
        <div className="row">
          <div className="col-xl-4">
            <ChartCard
              title="Titles"
              amount={title_count}
              chartProps={{
                width: 120,
                height: 107,
                lines: [
                  {
                    values: [2, 11, 8, 14, 18, 20, 26],
                    colors: {
                      area: 'rgba(199, 228, 255, 0.5)',
                      line: '#004585',
                    },
                  },
                ],
              }}
            />
          </div>
          <div className="col-xl-4">
            <ChartCard
              title="Actors"
              amount={actor_count}
              chartProps={{
                width: 120,
                height: 107,
                lines: [
                  {
                    values: [20, 80, 67, 120, 132, 66, 97],
                    colors: {
                      area: 'rgba(199, 228, 255, 0.5)',
                      line: '#004585',
                    },
                  },
                ],
              }}
            />
          </div>
          <div className="col-xl-4">
            <ChartCard
              title="Completed data"
              amount="$240.56"
              chartProps={{
                width: 120,
                height: 107,
                lines: [
                  {
                    values: [42, 40, 80, 67, 84, 20, 97],
                    colors: {
                      area: 'rgba(199, 228, 255, 0.5)',
                      line: '#004585',
                    },
                  },
                ],
              }}
            />
          </div>
          {items}
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
      </Authorize>
    )
  }
}

export default DashboardAlpha
