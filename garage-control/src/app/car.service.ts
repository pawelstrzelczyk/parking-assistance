import {Injectable} from '@angular/core';
import {Observable, of} from "rxjs";
import {Car} from "./model/car";
import {HttpClient} from "@angular/common/http";
import {AccessLog} from "./model/access-log";
import {GasLog} from "./model/gas-log";

@Injectable({
  providedIn: 'root'
})
export class CarService {

  constructor(
    private http: HttpClient
  ) {
  }

  public getAll(): Observable<Array<Car>> {
    return this.http.get<Array<Car>>(
      "http://127.0.0.1:5000/get-vehicles"
    )
  }

  public addCar(car: Car): Observable<any> {
    return this.http.post(
      "http://127.0.0.1:5000/add-vehicle/" + car.license_plate + "/" + car.length + "/" + car.width + "/" + car.hasAccess,
      null
    );
  }

  public changeAccess(car: Car): Observable<any> {
    return this.http.post(
      "http://127.0.0.1:5000/grant-access/" + car.license_plate + "/" + (car.hasAccess == 0 ? 1 : 0),
      null
    )
  }

  public delete(car: Car): Observable<any> {
    return this.http.delete(
      "http://127.0.0.1:5000/" + car.license_plate
    )
  }

  public getLogs(): Observable<Array<AccessLog>> {
    return this.http.get<Array<AccessLog>>(
      "http://127.0.0.1:5000/get-logs"
    )
  }

  public getGasLogs(): Observable<Array<GasLog>> {
    return this.http.get<Array<GasLog>>(
      "http://127.0.0.1:5000/get-gas-logs"
    );
  }
}
