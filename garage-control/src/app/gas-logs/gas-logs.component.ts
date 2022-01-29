import {Component, OnInit, ViewChild} from '@angular/core';
import {MatTableDataSource} from "@angular/material/table";
import {MatPaginator} from "@angular/material/paginator";
import {MatSort} from "@angular/material/sort";
import {GasLog} from "../model/gas-log";
import {CarService} from "../car.service";
import {AccessLog} from "../model/access-log";

@Component({
  selector: 'app-gas-logs',
  templateUrl: './gas-logs.component.html',
  styleUrls: ['./gas-logs.component.css']
})
export class GasLogsComponent implements OnInit {
  dataSource!: MatTableDataSource<GasLog>;
  displayedColumns: string[] = ['timestamp'];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;


  constructor(private carService: CarService) {
  }

  ngOnInit(): void {
    this.refresh();
  }

  public refresh(): void {
    this.carService.getGasLogs().subscribe(
      l => {
        this.dataSource = new MatTableDataSource<GasLog>(l);
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
      }
    )
  }

}
