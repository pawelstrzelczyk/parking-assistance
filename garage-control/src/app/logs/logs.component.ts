import {Component, OnInit, ViewChild} from '@angular/core';
import {AccessLog} from "../model/access-log";
import {CarService} from "../car.service";
import {MatTableDataSource} from "@angular/material/table";
import {MatPaginator} from "@angular/material/paginator";
import {MatSort} from "@angular/material/sort";

@Component({
  selector: 'app-logs',
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.css']
})
export class LogsComponent implements OnInit {

  dataSource!: MatTableDataSource<AccessLog>;
  displayedColumns: string[] = ['timestamp', 'licensePlate', 'isAllowed'];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private carService: CarService) {
  }

  ngOnInit(): void {
    this.refresh();
  }

  public refresh(): void {
    this.carService.getLogs().subscribe(
      l => {
        this.dataSource = new MatTableDataSource<AccessLog>(l);
        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
      }
    )
  }

}
