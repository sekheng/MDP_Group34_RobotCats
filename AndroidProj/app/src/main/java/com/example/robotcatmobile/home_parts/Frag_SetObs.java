package com.example.robotcatmobile.home_parts;

import android.os.Build;
import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.widget.AppCompatToggleButton;
import androidx.fragment.app.Fragment;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.example.robotcatmobile.R;

import java.util.ArrayList;

@RequiresApi(api = Build.VERSION_CODES.N)
public class Frag_SetObs extends Fragment {
    // the toggle buttons!
    ArrayList<AppCompatToggleButton> mArrayToggle = new ArrayList<>();

    public Frag_SetObs() {
        // Required empty public constructor
    }


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_set_obs, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        mArrayToggle.add(view.findViewById(R.id.obstacle_toggle));
        mArrayToggle.add(view.findViewById(R.id.robot_toggle));
        mArrayToggle.add(view.findViewById(R.id.direction_toggle));
        mArrayToggle.add(view.findViewById(R.id.type_toggle));

        for (int j = 0; j < mArrayToggle.size(); j++) {
            final AppCompatToggleButton toggleButton = mArrayToggle.get(j);
            toggleButton.setOnCheckedChangeListener((compoundButton, b) -> {
                    String toggleButtonTxt = compoundButton.getText().toString();
                    if (b) {
                        for (int i = 0; i < mArrayToggle.size(); i++) {
                            final AppCompatToggleButton otherToggle = mArrayToggle.get(i);
                            if (compoundButton != otherToggle)
                                otherToggle.setChecked(false);
                        }
                        // then set the state
                        for (SET_GRID_STATE state:SET_GRID_STATE.values()) {
                            if (toggleButtonTxt.contains(state.toString())) {
                                GridRecycler.curInteractState = state;
                                break;
                            }
                        }
                    }
                    else {
                        // then check and ensure that the buttons matched with the undex
                        if (toggleButtonTxt.contains(GridRecycler.curInteractState.toString()))
                        {
                            GridRecycler.curInteractState = SET_GRID_STATE.NONE;
                        }
                    }
                }
            );
        }
    }
}