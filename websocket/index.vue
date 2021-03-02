<template>
  <div class="dataDictionaryManagement">
    <div class="RoleManagementSearchPanel">
      <el-select
        v-model="companyId"
        clearable
        filterable
        style="margin-right:20px;width:300px"
        placeholder="请选择公司"
        size="medium"
        @change="selectChange"
      >
        <el-option
          v-for="item in companyOptions"
          :key="item.pkId"
          :label="item.companyName"
          :value="item.pkId"
        />
      </el-select>
      <FormPanel
        :ref="formConfigSearch.name"
        :form-config="formConfigSearch"
      >
        <template
          slot="operator"
          slot-scope="scope"
        >
          <div class="operator">
            <el-button
              type="primary"
              size="medium"
              @click="createWebSocket()"
            >
              1111111111
            </el-button>
            <el-button
              type="primary"
              size="medium"
              :disabled="disableAddBtn"
              @click="addData(scope)"
            >
              {{ addOrCancel }}
            </el-button>
            <UploadFile
              :uploadfile-conf="uploadfileConf"
              class="UploadFile"
            />
            <el-button
              size="medium"
              @click="deleteUserFun"
            >
              批量删除
            </el-button>
            <el-button
              type="primary"
              size="medium"
              @click="$api.downFile($api.dictExportAll,'数据字典.xls')"
            >
              导出
            </el-button>
          </div>
        </template>
      </FormPanel>
    </div>

    <div
      class="RoleManagementGrid"
      element-loading-text="数据加载中"
    >
      <GridPanel
        :ref="gridConf.name"
        v-loading="loading"
        :grid-data="gridData"
        :grid-conf="gridConf"
        @pagination="getAllListData"
      >
        <template v-slot:operator="scope">
          <div
            style="display: flex;justify-content: space-around"
            :class="{'disableBtn': disableBtn ===scope.scope.row.editing&& cancelBtn}"
          >
            <el-button
              v-show="!scope.scope.row.editing"
              type="text"
              style="color: #1890ff;"
              @click="dicDetailFunc(scope.scope)"
            >
              字典明细
            </el-button>

            <el-button
              v-show="!scope.scope.row.editing && scope.scope.row.canEdit"
              type="text"
              style="color: #1890ff;"
              @click="actionFun(scope.scope,'edit')"
            >
              编辑
            </el-button>
            <el-button
              v-show="scope.scope.row.editing"
              type="text"
              style="color: #1890ff;"
              @click="actionFun(scope.scope,'save')"
            >
              保存
            </el-button>
            <el-button
              v-show="scope.scope.row.editing && operatorType !== 'save'"
              type="text"
              style="color: #1890ff;"
              @click="actionFun(scope.scope,'cancel')"
            >
              取消
            </el-button>
            <el-button
              v-show="!scope.scope.row.editing && scope.scope.row.canEdit"
              type="text"
              style="color: #1890ff"
              @click="deleteUserFun(scope.scope)"
            >
              删除
            </el-button>
          </div>
        </template>
        <template v-slot:dictStatus="scope">
          <SwitchField

            :config="{
              activetext: '启用',
              inactivetext: '停用',
              disabled: scope.scope.row.disabled ||!scope.scope.row.canEdit ,
              value: scope.scope.row.dictStatus ,
              activevalue: 0,
              inactivevalue: 1,
              row: scope.scope.row,
              change: switchChange
            }"
          />
        </template>
        <template v-slot:dictName="scope">
          <el-input
            v-model.trim="scope.scope.row.dictName"
            placeholder="请输入内容"
          />
        </template>
        <template v-slot:dictDesc="scope">
          <el-input
            v-model.trim="scope.scope.row.dictDesc"
            placeholder="请输入内容"
          />
        </template>
        <template v-slot:dictCode="scope">
          <el-input
            v-model.trim="scope.scope.row.dictCode"
            placeholder="请输入内容"
          />
        </template>
      </GridPanel>
    </div>
    <el-dialog
      v-if="dialog.dialogVisible"
      :visible="dialog.dialogVisible"
      :title="dialog.title||'字典明细'"
      width="50%"
      class="diaDetail"
      @close="dialog.dialogVisible=false"
    >
      <dictionaryDetailForm
        ref="dicDetailForm"
        :data="dicDetailData"
      />
    </el-dialog>
  </div>
</template>

<script>
import dictionaryDetailForm from './dictionaryDetailForm'
import Sortable from 'sortablejs'
import { mapState } from 'vuex'
export default {
  inject: ['reload'],
  name: 'Roles',
  components: {
    dictionaryDetailForm
  },

  data() {
    return {
      companyId: '',
      companyOptions: [], // 公司
      disableAddBtn: false,
      cancelBtn: true,
      disableBtn: false,
      dialog: {
        dialogVisible: false,
        title: ''
      },
      dicDetailData: {},
      addOrCancel: '新增',
      operatorType: 'edit',
      loading: false,

      uploadfileConf: {
        btnName: '导入',
        templateHref: (fN) => {
          this.$api.downFile(this.$api.dictExcelDemoExport, fN)
        },
        templateName: '数据字典模板',
        uploadApi: this.$api.dictImportExcel,
        success: () => {
          this.reload()
        },
        catch: (e) => {
          this.$message.error(e)
        },
        fileName: '数据字典模板.xls'
      },

      formConfigSearch: {
        name: 'formConfigSearch',
        title: '',
        labelwidth: 0,
        marginLeft: 0,
        formWidth: 100,
        node: 1,
        inline: false,

        fields: [
          {
            children: [
              {
                field: 'user',
                xtype: 'TextField',
                fieldWidth: 30,
                placeholder: '请输入数据字典名称',
                node: [0],
                confirmBtn: '查询',
                clearable: true,
                confirm: this.searchConfirm
              },
              {
                fieldWidth: 70,
                slotName: 'operator'
              }
            ]
          }
        ]
      },

      // 表格配置
      gridData: [],
      gridConf: {
        rowKey: 'pkId',
        name: 'dataDictionaryGrid',
        url: '',
        editAble: false,
        headerClass: 'blueHead',
        height: 600,
        columns: [
          {
            label: '字典名称',
            required: true,
            field: 'dictName',
            editable: true,
            sort: true
          },
          {
            label: '字典编码',
            field: 'dictCode',
            sort: true,
            editable: false,
            required: true
          },
          {
            label: '字典类型',
            field: 'systemTag',
            sort: true,
            editable: false,
            required: false
          },
          {
            label: '所属公司',
            required: false,
            field: 'orgName',
            editable: false,
            sort: true
          },
          {
            label: '字典说明',
            field: 'dictDesc',
            editable: true
          },
          {
            label: '状态',
            field: 'dictStatus',
            slot: true,
            width: 100,
            fixed: 'right'
          },
          {
            label: '操作',
            field: 'operator',
            slot: true,
            width: 350,
            fixed: 'right'
          }
        ],
        dropCol: [
          {
            label: '多选',
            type: 'selection',
            field: 'selection',
            align: 'center'
          },
          {
            label: '字典名称',
            required: true,
            field: 'name',
            editable: true,
            sort: true
          },
          {
            label: '字典编码',
            field: 'codeType',
            sort: true
          },
          {
            label: '字典说明',
            field: 'description',
            editable: true
          },
          {
            label: '状态',
            field: 'dictStatus',
            slot: true,
            width: 100,
            fixed: 'right'
          },
          {
            label: '操作',
            field: 'operator',
            slot: true,
            width: 350,
            fixed: 'right'
          }
        ],

        stripe: false,
        border: true,
        multSelect: true,
        size: 'small',
        pagination: true,
        pageSize: 10,
        page: 1,
        total: 40,
        pageSizes: [10, 20, 30, 40, 50],
        checkSelectable: (row) => {
          return !!row.canEdit
        }
      },

      searchData: {
        page: 1,
        size: 10,
        dictName: ''
      }
    }
  },
  computed: {
    ...mapState({
      userPost: state => state.user.userPost,
      userInfoObj: state => state.user.userInfoObj
    })
  },
  mounted() {
    this.getAllListData()
  },
  created() {
    this.getCompanyList()
  },
  methods: {
    // 搜索数据
    searchConfirm(e) {
      this.searchData.dictName = e.value
      this.gridConf.page = 1
      this.gridConf.pageSize = 10
      this.getAllListData()
    },
    // 获取字典列表数据
    getAllListData() {
      this.loading = true
      this.searchData.page = this.gridConf.page
      this.searchData.size = this.gridConf.pageSize
      this.searchData.companyId = this.companyId
      this.$post(this.$api.dictPage + '?page=' + this.gridConf.page + '&size=' + this.gridConf.pageSize, this.searchData).then(
        (response) => {
          console.log(response)
          this.gridConf.total = response.total
          this.gridData = response.data
          // 转义
          if (this.gridData != null) {
            this.gridData.forEach(item => {
              if (item.systemTag === '0') {
                item.canEdit = !!this.userInfoObj.systemAdmin
              } else {
                item.canEdit = true
              }

              item.systemTag = this.flagToDetail(item.systemTag)
            })
          }
        }
      )
      setTimeout(() => {
        this.loading = false
      }, 300)
    },

    // 字典明细弹出框
    dicDetailFunc(scope) {
      this.dialog.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.dicDetailForm.setValue(scope.row)
      })
    },
    // 行拖拽
    rowDrop() {
      const tbody = document.querySelector('.el-table__body-wrapper tbody')
      const _this = this
      Sortable.create(tbody, {
        onEnd({ newIndex, oldIndex }) {
          const currRow = _this.gridData.splice(oldIndex, 1)[0]
          _this.gridData.splice(newIndex, 0, currRow)
        }
      })
    },
    // 列拖拽
    columnDrop() {
      const wrapperTr = document.querySelector('.el-table__header-wrapper tr')

      this.sortable = Sortable.create(wrapperTr, {
        animation: 180,
        delay: 0,

        onEnd: (evt) => {
          const oldItem = this.gridConf.dropCol[evt.oldIndex]
          this.gridConf.dropCol.splice(evt.oldIndex, 1)
          this.gridConf.dropCol.splice(evt.newIndex, 0, oldItem)
        }
      })
    },
    addUserFun() {
      this.dialogConf.visable = true
    },

    // 删除，批量删除
    deleteUserFun(scope) {
      if (scope.row) {
        if (scope.row.pkId) {
          this.$confirm('是否要删除字典"' + scope.row.dictName + '"', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          })
            .then(() => {
              this.$delete(
                this.$api.dictUpdate + scope.row.pkId
              ).then(() => {
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                })
                this.getAllListData()
              })
            })
            .catch(() => {
            })
        }
      } else {
        // 批量删除
        const selection = this.$refs[this.gridConf.name].getSelection()
        const delArray = []
        selection.forEach((item) => {
          delArray.push(item.pkId)
        })
        if (delArray.length === 0) {
          this.$message({
            message: '请选择数据',
            type: 'warning'
          })
        } else {
          this.$confirm('是否要删除这' + delArray.length + '条数据', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          })
            .then(() => {
              this.$delete(this.$api.dictUpdate + delArray).then(
                () => {
                  this.$message({
                    type: 'success',
                    message: '删除成功!'
                  })
                  this.getAllListData()
                }
              )
            })
            .catch(() => {
            })
        }
      }
    },

    // 编辑，保存，取消
    actionFun: function(scope, action) {
      const row = {}
      switch (action) {
        case 'edit':
          this.gridConf.columns[1].editable = false // 字典编码不能编辑
          scope.row.disabled = true
          this.beforeEditRowDataCancel = JSON.parse(JSON.stringify(scope.row))
          this.$refs[this.gridConf.name].setRowEditable(scope.$index)
          this.disableBtn = false // 其他行按钮变灰
          this.cancelBtn = true // 取消按钮
          this.disableAddBtn = true // 新增按钮置灰色
          break
        case 'save':
          scope.row.disabled = false
          const flag = this.$refs[this.gridConf.name].setRowUnEditable(
            scope.$index,
            this.gridConf,
            scope
          )
          if (flag) {
            const data = scope.row
            if (data.pkId) {
              data.systemTag = this.detailToFlag(data.systemTag)
              this.$put(this.$api.dictUpdate + data.pkId, data)
                .then(() => {
                  this.$message({
                    message: '编辑成功',
                    type: 'success'
                  })
                  this.getAllListData()
                })
                .catch(() => {
                  this.getAllListData()
                })
            } else {
              data.codeType = '0'
              this.$post(this.$api.dictUpdate, data)
                .then(() => {
                  this.$message({
                    message: '新增成功',
                    type: 'success'
                  })
                  this.getAllListData()
                })
                .catch(() => {
                  this.getAllListData()
                })
            }
            this.addOrCancel = '新增'
            this.operatorType = 'edit'
            this.disableBtn = true
            this.cancelBtn = true
            this.disableAddBtn = false
          }
          break
        case 'cancel':
          scope.row.disabled = false
          this.disableBtn = false
          this.cancelBtn = false
          this.disableAddBtn = false
          this.getAllListData()
          break
      }
    },

    // 启用停用
    switchChange(e, data) {
      if (data.pkId) {
        this.$confirm('是否要执行？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(() => {
            data.dictStatus = e
            data.systemTag = this.detailToFlag(data.systemTag)
            console.log(data)
            this.$put(this.$api.dictUpdate + data.pkId, data).then(() => {
              this.$message({
                message: '成功',
                type: 'success'
              })
              this.getAllListData()
            }).catch((e) => {
              this.gridData = []
              this.getAllListData()
            })
          })
          .catch((e) => {
            this.gridData = []
            this.getAllListData()
          })
      }
    },

    // 新增数据
    addData() {
      if (this.operatorType !== 'save') {
        this.gridConf.columns[1].editable = true // 新增字典编码能编辑
        this.addOrCancel = '取消新增'
        this.operatorType = 'save'
        this.disableBtn = false
        this.cancelBtn = true
        const addData = {
          id: null,
          busSys: '',
          codeType: '',
          createTime: '',
          createUser: '',
          name: '',
          dictStatus: '0'
        }
        this.gridData.push(addData)

        this.$refs[this.gridConf.name].setRowEditable(this.gridData.length - 1)
        this.$nextTick(() => {
          const container = this.$el.querySelector('.el-table__body-wrapper')
          container.scrollTop = container.scrollHeight
        })
      } else {
        this.addOrCancel = '新增'
        this.operatorType = 'edit'
        this.disableBtn = false
        this.cancelBtn = false
        if(this.gridData[this.gridData.length-1].id === null){
            this.gridData.pop()
        }
        this.$nextTick(() => {
          const container = this.$el.querySelector('.el-table__body-wrapper')
          container.scrollTop = 0
        })
      }
    },
    flagToDetail(item) {
      return item === '0' ? '基础字典' : '公司字典'
    },
    detailToFlag(item) {
      return item === '基础字典' ? '0' : '1'
    },
    // 获取公司列表
    getCompanyList() {
      this.$get(this.$api.companyList).then((res) => {
        this.companyOptions = res
        return res
      })
    },
    selectChange(e) {
      this.gridConf.page = 1
      this.getAllListData()
    },
    // 与websocket服务器创建连接
    createWebSocket() {
      // 注意这里的端口号是后端服务的端口号，后面的是后端正常请求的路径，base是我的项目名，最后面的是我放在cookie中的当前登陆用户
      let websocket = new WebSocket('ws://127.0.0.1:8088/base/webSocket/luxc' )
      // 连接成功时
      websocket.onopen = () => {
        websocket.send('hello')
      }
      websocket.onmessage = event => {
        // 后端发送的消息在event.data中
        console.log(event.data)
      }
      websocket.onclose = function () {
        console.log('关闭了')
      }
      // 路由跳转时结束websocket链接
      this.$router.afterEach(function () {
        websocket.close()
      })
      // 监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常
      window.onbeforeunload = function () {
        websocket.close()
      }
    }

  }
}
</script>

<style lang="scss" scoped>
.disableBtn {
  button {
    color: #c5c8cd !important;
    pointer-events: none;
    cursor: not-allowed;
  }
}

.dataDictionaryManagement {
  height: 100%;
  padding: 50px;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;

  /deep/ .el-form-item {
    margin-bottom: 0;
  }

  .operator {
    text-align: right;

    .UploadFile {
      text-align: left;
    }
  }

  .RoleManagementSearchPanel {
    display: flex;
    margin-bottom: 10px;
  }

  .RoleManagementGrid {
    height: 80%;
    flex: 1;
  }

  .diaDetail {
    /deep/ .el-table {
      height: 350px;
    }
  }
}
</style>
